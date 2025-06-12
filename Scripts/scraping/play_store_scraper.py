import os
from google_play_scraper import reviews_all, Sort
import pandas as pd
from datetime import datetime

# Get project root dynamically
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")

# Ensure correct directory exists
os.makedirs(RAW_DATA_DIR, exist_ok=True)

BANK_APPS = {
    "Commercial Bank of Ethiopia": "com.combanketh.mobilebanking",
    "Bank of Abyssinia": "com.boa.boaMobileBanking",
    "Dashen Bank": "com.dashen.dashensuperapp"
}

def scrape_reviews(bank_name, app_id, count=100):
    """Scrape reviews from Google Play Store"""
    try:
        print(f"Scraping reviews for {bank_name}...")
        reviews = reviews_all(app_id, sleep_milliseconds=1000, lang="en", country="us", sort=Sort.NEWEST)

        if not reviews:
            print(f"No reviews found for {bank_name}")
            return pd.DataFrame()

        df = pd.DataFrame(reviews)
        df = df.rename(columns={"content": "review", "score": "rating", "at": "date"})[["review", "rating", "date"]]
        df["bank"] = bank_name
        df["source"] = "Google Play"

        return df.head(count)

    except Exception as e:
        print(f"Error scraping {bank_name}: {str(e)}")
        return pd.DataFrame()

def main():
    all_reviews = pd.DataFrame()

    for bank_name, app_id in BANK_APPS.items():
        bank_reviews = scrape_reviews(bank_name, app_id, count=100)
        all_reviews = pd.concat([all_reviews, bank_reviews], ignore_index=True)

    # Ensure proper path before saving
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_file = os.path.join(RAW_DATA_DIR, f"bank_reviews_raw_{timestamp}.csv")
    
    all_reviews.to_csv(raw_file, index=False)
    print(f"\nScraping completed. Saved {len(all_reviews)} reviews to {raw_file}")

if __name__ == "__main__":
    main()
