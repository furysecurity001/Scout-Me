# SCOUT-ME v2.6 - Google Maps Lead Generation Tool

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-1.40+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

[![Contact](https://img.shields.io/badge/Contact-@furysec-2CA5E0?logo=telegram&logoColor=white)](https://t.me/furysec)


## 📌 Overview

**SCOUT-ME** is a powerful lead generation tool that scrapes Google Maps to find businesses **without proper websites** - perfect for web developers, digital agencies, and marketers looking to offer website development services.

It identifies two types of leads:
- ✅ Businesses with **no website** at all
- ◆ Businesses using **social media / free builder** pages
╔══════════════════════════════════════════════════════════════════════════════╗
║ ███████╗ ██████╗ ██████╗ ██╗ ██╗████████╗ ███╗ ███╗███████╗ ║
║ ██╔════╝██╔═══██╗██╔══██╗██║ ██║╚══██╔══╝ ████╗ ████║██╔════╝ ║
║ ███████╗██║ ██║██║ ██║██║ ██║ ██║ ██╔████╔██║█████╗ ║
║ ╚════██║██║ ██║██║ ██║██║ ██║ ██║ ██║╚██╔╝██║██╔══╝ ║
║ ███████║╚██████╔╝██████╔╝╚██████╔╝ ██║ ██║ ╚═╝ ██║███████╗ ║
║ ╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚═╝ ╚═╝ ╚═╝╚══════╝ V2.6 ║
╚══════════════════════════════════════════════════════════════════════════════╝


## 🎯 Key Features

- 🔍 Scrapes Google Maps for businesses by category and location
- 🚫 Filters businesses with no website or only social media/free builder sites
- 📞 Extracts business names and phone numbers (multiple detection patterns)
- 💾 Saves leads in both **CSV** and **TXT** formats
- 🖥️ Beautiful interactive CLI with Rich library
- 🌐 Works for any country, state, and business category
- ⚡ Headless mode for fast background operation
- 🛡️ Auto-handles Google consent/cookie pages
- 🔗 Direct URL scraping for reliable data extraction
- 📜 Smart scrolling collects all listing URLs before processing

### 🏷️ Unofficial Websites Detected

Businesses using these platforms are flagged as potential leads:

| Category | Platforms |
|----------|-----------|
| Social Media | Facebook, Instagram, Twitter/X, LinkedIn, TikTok |
| Messaging | WhatsApp (wa.me) |
| Bio Links | Linktree, Carrd, About.me |
| Free Builders | Wix, Weebly, WordPress.com, Blogspot, Google Sites |



## 🚀 Quick Start

### Prerequisites
- **Python 3.8 or higher** - [Download](https://www.python.org/downloads/)
- **pip** (comes with Python)

### Installation

#### Option 1: From Source
```bash
# 1. Download and extract ScoutME_v2.6.zip
# 2. Open terminal in the extracted folder

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Playwright Chromium browser
python -m playwright install chromium

# 5. Run the tool
python scout_me.py
```
#### Option 2: From Source
```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium
python scout_me.py

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
python3 scout_me.py
```


## 📁 Project Structure
scout-me/

├── scout_me.py # Main application

├── requirements.txt # Python dependencies

├── README.md # This file

└── leads/ # Output directory (auto-created)

├── *.txt

└── *.csv

📖 Usage Guide
Interactive Mode
Launch the tool and follow the prompts:
```bash
python scout_me.py
```
Prompt	Default	Example
Target Country	Nigeria	USA, UK, Ghana, Kenya
State / City	Abuja	Lagos, New York, London
Business Category	Salon	Plumbers, Gyms, Restaurants
Maximum leads to collect	20	50, 100
Run in headless mode?	No	Yes (runs in background)

**Command-Line Mode**

```bash
python scout_me.py -q "Plumbers in Lagos, Nigeria" -m 30 --headless
```

Flag	Description	Default
-q, --query	Search query	Required
-m, --max	Maximum leads to collect	20
--headless	Run browser in background	False
