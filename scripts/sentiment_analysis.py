# sentiment_analysis.py

import pandas as pd
from transformers import pipeline

# Update this path if needed
csv_path = "../data/processed/bank_reviews_clean_20250612_200200.csv"
output_path = "../data/analyzed/sentiment_results.csv"

# Load the reviews
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# Load the sentiment classifier
try:
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Apply sentiment classification
def classify_sentiment(text):
    try:
        result = classifier(text[:512])[0]  # Truncate long text
        return result['label'].lower(), round(result['score'], 4)
    except:
        return "neutral", 0.5

# Apply the function to each review
df[['sentiment', 'confidence']] = df['review'].astype(str).apply(lambda x: pd.Series(classify_sentiment(x)))

# Save to CSV
try:
    df.to_csv(output_path, index=False)
    print(f"Saved sentiment results to {output_path}")
except Exception as e:
    print(f"Error saving file: {e}")
