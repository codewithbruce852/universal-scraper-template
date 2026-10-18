"""
Universal Web Scraper Template
------------------------------
A production-ready template for scraping static websites.
Change the CONFIGURATION section to scrape any site.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import csv
from datetime import datetime

# ==========================================
# ⚙️ CONFIGURATION (Change this for each job)
# ==========================================
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
START_PAGE = 1
END_PAGE = 3  # How many pages to scrape
OUTPUT_FILE = "scraped_data.csv"

# You find these using Chrome "Inspect Element"
ITEM_SELECTOR = "article.product_pod"     # The box holding one item
TITLE_SELECTOR = "h3 a"                   # The title inside the box
PRICE_SELECTOR = ".price_color"           # The price inside the box
LINK_SELECTOR = "h3 a"                    # The link inside the box

# ==========================================
# 🛠️ CORE FUNCTIONS (Don't change these)
# ==========================================

def fetch_page(url):
    """Downloads the HTML and handles basic blocking."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Check for 404, 403, 500 errors
        response.encoding = "utf-8" # Fix weird symbols like £ or €
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

def parse_page(html, page_num, base_url):
    """Extracts data from the HTML."""
    soup = BeautifulSoup(html, "lxml")
    items = soup.select(ITEM_SELECTOR)
    
    extracted_data = []
    
    for item in items:
        # Extract Title
        title_el = item.select_one(TITLE_SELECTOR)
        title = title_el.get("title", title_el.text.strip()) if title_el else "N/A"
        
        # Extract Price
        price_el = item.select_one(PRICE_SELECTOR)
        price = price_el.text.strip() if price_el else "N/A"
        
        # Extract Link
        link_el = item.select_one(LINK_SELECTOR)
        link = link_el["href"] if link_el else "N/A"
        
        # If the link is relative, make it absolute
        if link != "N/A" and link.startswith("/") or ".." in link:
            # Quick cleanup for relative links (varies by site)
            link = base_url.split("catalogue")[0] + link.replace("../", "")

        extracted_data.append({
            "Title": title,
            "Price": price,
            "URL": link,
            "Scraped_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    return extracted_data

def save_data(data, filename):
    """Saves the list of dictionaries to a CSV."""
    if not data:
        print("⚠️ No data to save.")
        return
        
    df = pd.DataFrame(data)
    # Remove duplicates based on Title (optional, but good for QA)
    df = df.drop_duplicates(subset=["Title"])
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"\n💾 Successfully saved {len(df)} records to {filename}")

# ==========================================
# 🚀 MAIN RUNNER
# ==========================================

def run_scraper():
    print(f"🚀 Starting Scraper: {BASE_URL}")
    all_results = []
    
    for page in range(START_PAGE, END_PAGE + 1):
        print(f"📄 Scraping page {page}...")
        url = BASE_URL.format(page)
        
        html = fetch_page(url)
        if not html:
            print("⏭️ Skipping page due to error.")
            continue
            
        page_data = parse_page(html, page, BASE_URL)
        all_results.extend(page_data)
        
        print(f"   ✅ Found {len(page_data)} items.")
        
        # Polite delay to avoid getting blocked (1 to 3 seconds)
        time.sleep(random.uniform(1.0, 3.0))
        
    save_data(all_results, OUTPUT_FILE)
    print("🎉 Done!")

if __name__ == "__main__":
    run_scraper()