import os
import pandas as pd
from datetime import datetime

def get_project_root():
    """Returns project root where 'data/raw/' exists"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def load_latest_raw_data():
    """Find and load the latest raw data file"""
    raw_dir = os.path.join(get_project_root(), "data", "raw")

    raw_files = [f for f in os.listdir(raw_dir) if f.startswith("bank_reviews_raw") and f.endswith(".csv")]

    if not raw_files:
        raise FileNotFoundError(f"No raw data files found in {raw_dir}")

    latest_file = sorted(raw_files)[-1]
    file_path = os.path.join(raw_dir, latest_file)

    if os.path.getsize(file_path) == 0:
        raise ValueError(f"File is empty: {file_path}")

    print(f"✅ Loading {latest_file}...")
    return pd.read_csv(file_path)

def main():
    project_root = get_project_root()
    processed_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    raw_df = load_latest_raw_data()

    if raw_df is None or raw_df.empty:
        print("\n💥 No valid data found. Exiting.")
        return

    # Save cleaned data correctly inside 'data/processed/'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    processed_file = os.path.join(processed_dir, f"bank_reviews_clean_{timestamp}.csv")

    raw_df.to_csv(processed_file, index=False)
    print(f"\n✅ Successfully saved cleaned data to: {processed_file}")

if __name__ == "__main__":
    main()
