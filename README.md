# SCOUT-ME v2.6 - Google Maps Lead Generation Tool

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-1.40+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📌 Overview

**SCOUT-ME** is a powerful lead generation tool that scrapes Google Maps to find businesses **without proper websites** - perfect for web developers, digital agencies, and marketers looking to offer website development services.

### 🎯 Key Features
- 🔍 Scrapes Google Maps for businesses by category and location
- 🚫 Filters businesses with no website or only social media/free builder sites
- 📞 Extracts business names and phone numbers
- 💾 Saves leads in both CSV and TXT formats
- 🖥️ Interactive CLI with beautiful UI (Rich library)
- 🌐 Support for any country, state, and business category
- ⚡ Headless mode for background operation
- 🛡️ Auto-handles Google consent pages
- 🔗 Direct URL scraping for reliable data extraction

### 🏷️ Unofficial Websites Detected
Businesses using these are flagged as leads:
- **Social Media:** Facebook, Instagram, Twitter/X, LinkedIn, TikTok
- **Messaging:** WhatsApp (wa.me)
- **Bio Links:** Linktree, Carrd, About.me
- **Free Builders:** Wix, Weebly, WordPress.com, Blogspot, Google Sites

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

#### **Option 1: From Source**
```bash
# 1. Download and extract ScoutME_v2.6.zip
# 2. Open terminal in the extracted folder

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
python -m playwright install chromium

# 5. Run the tool
python scout_me.py
