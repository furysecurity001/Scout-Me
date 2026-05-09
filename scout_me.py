from playwright.sync_api import sync_playwright
import time
import csv
from pathlib import Path
from datetime import datetime
from typing import List
from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, IntPrompt, Confirm
from rich import print as rprint
import random
from urllib.parse import quote_plus

console = Console()

UNOFFICIAL_DOMAINS = ['sites.google.com', 'facebook.com', 'instagram.com', 'twitter.com',
                      'linkedin.com', 'youtube.com', 'tiktok.com', 'wa.me', 'linktr.ee']

@dataclass
class Lead:
    name: str
    phone: str
    address: str
    website: str
    maps_link: str
    query: str
    timestamp: str
    category: str
    location: str


class ScoutMeScraper:
    BANNER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║   ███████╗ ██████╗ ██████╗ ██╗   ██╗████████╗    ███╗   ███╗███████╗       ║
║   ██╔════╝██╔═══██╗██╔══██╗██║   ██║╚══██╔══╝    ████╗ ████║██╔════╝       ║
║   ███████╗██║   ██║██║  ██║██║   ██║   ██║       ██╔████╔██║█████╗         ║
║   ╚════██║██║   ██║██║  ██║██║   ██║   ██║       ██║╚██╔╝██║██╔══╝         ║
║   ███████║╚██████╔╝██████╔╝╚██████╔╝   ██║       ██║ ╚═╝ ██║███████╗       ║
║   ╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝       ╚═╝     ╚═╝╚══════╝ V2.6  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

    def __init__(self, headless: bool = False, delay: float = 1.5):
        self.headless = headless
        self.delay = delay
        self.leads: List[Lead] = []
        self.start_time = datetime.now()

    def display_banner(self):
        console.print(self.BANNER, style="bold cyan")
        console.print(Panel.fit(
            "[bold red]LEAD GENERATION TOOL[/bold red]\n"
            "[dim]Find businesses without proper websites[/dim]",
            border_style="red"
        ))
        rprint("[bold green]Developed by Fury Security | Telegram: (t.me/furysec)[/bold green] | [dim]SCOUT-ME v2.6[/dim]\n")

    def get_user_input(self):
        country     = Prompt.ask("[cyan]Target Country", default="Nigeria")
        state_city  = Prompt.ask("[cyan]State / City", default="Abuja")
        category    = Prompt.ask("[cyan]Business Category", default="Salon")
        max_results = IntPrompt.ask("[cyan]Maximum leads to collect", default=20)
        headless    = Confirm.ask("[cyan]Run in headless mode?", default=False)
        return country, state_city, category, max_results, headless

    def _goto(self, page, url: str):
        for attempt in range(3):
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                time.sleep(3)
                return
            except Exception as e:
                console.print(f"[yellow]⚠️  Load attempt {attempt+1}/3 failed: {str(e)[:80]}[/yellow]")
                if attempt == 2:
                    raise
                time.sleep(4)

    def _dismiss_consent(self, page):
        for _ in range(6):
            if "consent.google" not in page.url.lower():
                return
            for sel in [
                'button[aria-label="Accept all"]', "#L2AGLb",
                'button:has-text("Accept all")', 'button:has-text("Agree")',
            ]:
                try:
                    btn = page.locator(sel).first
                    if btn.count() > 0 and btn.is_visible(timeout=2000):
                        btn.click(timeout=8000)
                        time.sleep(3)
                        break
                except:
                    continue
            else:
                time.sleep(2)

    def _scroll_feed(self, page, max_results: int):
        """Scroll the feed panel until we have enough cards or it stops growing."""
        feed = page.locator('div[role="feed"]')
        prev = 0
        stale = 0
        while stale < 4:
            feed.evaluate("el => el.scrollBy(0, 1500)")
            time.sleep(self.delay + random.uniform(0.2, 0.6))
            cards = page.locator('div[role="feed"] a[href*="/maps/place/"]').all()
            console.print(f"[dim]  Cards visible: {len(cards)}[/dim]")
            if len(cards) >= max_results * 3:
                break
            if len(cards) == prev:
                stale += 1
            else:
                stale = 0
            prev = len(cards)
        return page.locator('div[role="feed"] a[href*="/maps/place/"]').all()

    def _extract_lead(self, page, url: str, query: str, category: str, location: str):
        """
        Navigate directly to a listing URL and extract data.
        Returns a Lead or None.
        """
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(1.5 + random.uniform(0.2, 0.5))
        except:
            return None

        # Name
        try:
            h1 = page.locator('h1').first
            name = h1.inner_text(timeout=5000).strip() if h1.count() > 0 else ""
        except:
            name = ""
        if not name:
            return None

        # Phone — try multiple patterns
        phone = "N/A"
        try:
            # Pattern 1: role=link name=Call
            ph = page.get_by_role("link", name="Call").first
            if ph.count() > 0:
                href = ph.get_attribute("href") or ""
                phone = href.replace("tel:", "").strip()
        except:
            pass
        if phone == "N/A":
            try:
                # Pattern 2: any tel: href on the page
                tel_links = page.locator('a[href^="tel:"]').all()
                if tel_links:
                    phone = (tel_links[0].get_attribute("href") or "").replace("tel:", "").strip()
            except:
                pass
        if phone == "N/A":
            try:
                # Pattern 3: aria-label containing phone digits
                el = page.locator('[data-item-id^="phone"]').first
                if el.count() > 0:
                    phone = (el.get_attribute("aria-label") or "").replace("Phone:", "").strip()
            except:
                pass

        # Website
        website = "None"
        try:
            ws = page.get_by_role("link", name="Website").first
            if ws.count() > 0:
                website = ws.get_attribute("href") or "None"
        except:
            pass
        if website == "None":
            try:
                # Fallback: data-item-id="authority"
                el = page.locator('[data-item-id="authority"]').first
                if el.count() > 0:
                    website = el.get_attribute("href") or "None"
            except:
                pass

        # Filter: only keep businesses with no website or only social/unofficial
        has_no_site  = website == "None"
        has_bad_site = any(d in website.lower() for d in UNOFFICIAL_DOMAINS)
        if not (has_no_site or has_bad_site):
            return None

        return Lead(
            name=name, phone=phone, address="N/A",
            website=website, maps_link=page.url,
            query=query, timestamp=datetime.now().isoformat(),
            category=category, location=location
        )

    def scrape(self, query: str, max_results: int, category: str, location: str) -> List[Lead]:
        self.leads = []

        with sync_playwright() as p:
            console.print("[yellow]⏳ Launching browser...[/yellow]")
            browser = p.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-dev-shm-usage',
                      '--disable-blink-features=AutomationControlled',
                      '--dns-prefetch-disable', '--disable-extensions']
            )
            context = browser.new_context(
                viewport={"width": 1440, "height": 900},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                locale="en-US",
                timezone_id="Africa/Lagos",
            )
            context.add_cookies([{
                "name": "SOCS",
                "value": "CAISHAgBEhJnd3NfMjAyNDAxMTUtMF9SQzEaAmVuIAEaBgiA_LKsBg",
                "domain": ".google.com",
                "path": "/",
            }])

            # ── Phase 1: load search results and collect listing URLs ──
            search_page = context.new_page()
            search_url  = f"https://www.google.com/maps/search/{quote_plus(query)}/"
            console.print(f"[yellow]🌐 Opening: {search_url}[/yellow]")

            try:
                self._goto(search_page, search_url)
                console.print(f"[dim]URL after load: {search_page.url}[/dim]")

                if "consent.google" in search_page.url.lower():
                    self._dismiss_consent(search_page)
                    self._goto(search_page, search_url)

                console.print("[yellow]⏳ Waiting for results feed...[/yellow]")
                try:
                    search_page.wait_for_selector('div[role="feed"]', timeout=25000)
                    console.print("[green]✓ Results feed loaded.[/green]")
                except:
                    console.print("[red]❌ Results feed never appeared.[/red]")
                    search_page.screenshot(path="debug_no_feed.png")
                    browser.close()
                    return []

                console.print("[yellow]📜 Scrolling to collect listing URLs...[/yellow]")
                cards = self._scroll_feed(search_page, max_results)
                console.print(f"[green]✓ Found {len(cards)} candidate cards.[/green]")

                # Extract hrefs while page is still open
                listing_urls = []
                for card in cards:
                    try:
                        href = card.get_attribute("href") or ""
                        if href and href not in listing_urls:
                            listing_urls.append(href)
                    except:
                        continue

                console.print(f"[green]✓ Collected {len(listing_urls)} unique listing URLs.[/green]")

            finally:
                search_page.close()

            if not listing_urls:
                console.print("[red]❌ No listing URLs found.[/red]")
                browser.close()
                return []

            # ── Phase 2: visit each listing and extract data ────────────
            detail_page = context.new_page()

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("{task.completed}/{task.total} leads"),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Collecting leads...", total=max_results)

                processed_names = set()

                for url in listing_urls:
                    if len(self.leads) >= max_results:
                        break

                    console.print(f"[dim]→ Checking: {url[:80]}[/dim]")
                    lead = self._extract_lead(detail_page, url, query, category, location)

                    if lead is None:
                        console.print(f"[dim]  ✗ Skipped (has proper website or no name)[/dim]")
                        continue

                    if lead.name in processed_names:
                        console.print(f"[dim]  ✗ Duplicate: {lead.name}[/dim]")
                        continue

                    processed_names.add(lead.name)
                    self.leads.append(lead)
                    progress.update(task, completed=len(self.leads))

                    icon = "[green]✓[/green]" if lead.website == "None" else "[yellow]◆[/yellow]"
                    rprint(f"{icon} {lead.name[:48]:<48} | {lead.phone} | {lead.website}")

                progress.update(task, completed=len(self.leads))

            detail_page.close()
            browser.close()
            console.print("[dim]✓ Browser closed.[/dim]")

        return self.leads[:max_results]


def save_leads(leads: List[Lead], category: str, location: str, output_dir: str = "leads"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    base = f"{category.replace(' ', '_')}_{location.replace(' ', '_')}_{timestamp}"
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(output_path / f"{base}.txt", "w", encoding="utf-8") as f:
        f.write("SCOUT-ME v2.6 LEAD REPORT\n")
        f.write("=" * 90 + "\n")
        f.write(f"Query : {category} in {location}\n")
        f.write(f"Date  : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Total : {len(leads)}\n")
        f.write("=" * 90 + "\n\n")
        for i, lead in enumerate(leads, 1):
            f.write(f"#{i} {lead.name}\n   Phone   : {lead.phone}\n   Website : {lead.website}\n   Maps    : {lead.maps_link}\n\n")

    with open(output_path / f"{base}.csv", "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Website", "Maps Link"])
        for lead in leads:
            writer.writerow([lead.name, lead.phone, lead.website, lead.maps_link])

    console.print(f"[green]✓ Saved {len(leads)} leads → [bold]{output_dir}/{base}.csv[/bold][/green]")


def main():
    scraper = ScoutMeScraper()
    scraper.display_banner()
    country, state_city, category, max_results, headless = scraper.get_user_input()
    scraper.headless = headless
    location = f"{state_city}, {country}"
    query    = f"{category} in {location}"

    console.print(f"\n[bold green]🎯 Target: {query} | Max {max_results} leads[/bold green]\n")

    leads = scraper.scrape(query, max_results, category, location)

    if leads:
        save_leads(leads, category, location)
        duration = (datetime.now() - scraper.start_time).total_seconds()
        console.print(f"\n[bold green]✅ DONE! Collected {len(leads)} leads in {duration:.1f}s[/bold green]")
    else:
        console.print("\n[bold red]❌ No leads collected.[/bold red]")
        console.print("[yellow]→ All businesses found may have proper websites — try a different category[/yellow]")
        console.print("[yellow]→ Check debug_no_feed.png if the feed never loaded[/yellow]")

if __name__ == "__main__":
    main()