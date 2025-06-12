import os
import pandas as pd
from google_play_scraper import reviews_all, Sort, app
from datetime import datetime
import time

# Configure paths and parameters
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '../../data/raw')  # Goes up two levels to project root
os.makedirs(DATA_DIR, exist_ok=True)

# Updated bank apps with multiple package name options
BANK_APPS = {
    "Commercial Bank of Ethiopia": [
        "com.combanketh.mobilebanking",
        "com.cbe.android.cbe",  # Most likely current ID
        "com.cbe.cbe"          # Legacy ID
    ],
    "Bank of Abyssinia": [
        "com.boa.boaMobileBanking",
        "com.bankofabyssinia.mobilebanking",
        "com.bankofabyssinia"
    ],
    "Dashen Bank": [
        "com.dashen.dashensuperapp",
        "com.dashenbank.smartbank",
        "com.dashenmobile.dashen"
    ]
}

# Countries to try (Ethiopia first)
COUNTRIES = ['et', 'us', 'ke', 'za', 'ng']

def verify_app(package_list):
    """Check if any package exists and return the first valid ID."""
    for package_name in package_list:
        try:
            result = app(package_name)
            return package_name if result else None
        except:
            continue
    return None

def scrape_reviews(app_id, country, max_retries=3):
    """Scrape reviews with retries and error handling."""
    for attempt in range(max_retries):
        try:
            reviews = reviews_all(
                app_id,
                lang='en',
                country=country,
                sort=Sort.NEWEST,
                sleep_milliseconds=2000,
                count=200
            )
            return reviews
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                print(f"Attempt {attempt + 1} failed. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            print(f"Final attempt failed for {app_id} in {country}: {str(e)}")
            return []

def main():
    all_reviews = pd.DataFrame()
    
    for bank_name, package_options in BANK_APPS.items():
        print(f"\n{'='*40}\nProcessing {bank_name}\n{'='*40}")
        
        valid_app_id = verify_app(package_options)
        if not valid_app_id:
            print(f"⚠️ No valid package found for {bank_name}. Skipping...")
            continue
            
        for country in COUNTRIES:
            print(f"\nTrying {country.upper()} store...")
            reviews = scrape_reviews(valid_app_id, country)
            
            if reviews:
                df = pd.DataFrame(reviews)
                
                col_map = {'content': 'review', 'score': 'rating', 'at': 'date'}
                df = df.rename(columns={k:v for k,v in col_map.items() if k in df.columns})
                
                df['bank'] = bank_name
                df['source'] = f'Google Play ({country.upper()})'
                
                final_cols = ['review', 'rating', 'date', 'bank', 'source']
                df = df[[c for c in final_cols if c in df.columns]]
                
                all_reviews = pd.concat([all_reviews, df], ignore_index=True)
                print(f"✅ Found {len(df)} reviews")
                break
            else:
                print(f"❌ No reviews found in {country.upper()}")

    if not all_reviews.empty:
        all_reviews = all_reviews.drop_duplicates(subset=['review', 'bank'])
        all_reviews['date'] = pd.to_datetime(all_reviews['date']).dt.strftime('%Y-%m-%d')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(DATA_DIR, f'bank_reviews_{timestamp}.csv')
        all_reviews.to_csv(output_file, index=False)
        
        print(f"\n{'='*40}")
        print(f"🎉 Successfully collected {len(all_reviews)} reviews")
        print(f"📁 Saved to: {os.path.abspath(output_file)}")
        print(f"{'='*40}")
    else:
        print("\n⚠️ No reviews collected. Possible solutions:")
        print("1. Use a VPN with an Ethiopian IP address")
        print("2. Collect reviews manually from Play Store")
        print("3. Consult facilitators for a sample dataset")

if __name__ == "__main__":
    main()
