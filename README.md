# 🕷️ Universal Web Scraper Template

A production-ready Python web scraping template designed for rapid deployment of custom scraping projects. 

Instead of writing a script from scratch, this template allows you to configure 4 variables at the top of the file to scrape almost any static website.

## ✨ Features

- **Configurable:** Just change the URL and CSS selectors.
- **Robust Fetching:** Includes browser User-Agent headers to avoid basic 403 blocks.
- **Encoding Safe:** Forces UTF-8 decoding to prevent weird characters (like £, €, ¥).
- **Polite Scraping:** Includes randomized delays between page requests to avoid getting IP-banned.
- **Clean Output:** Automatically exports to a deduplicated CSV with a timestamp.

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt