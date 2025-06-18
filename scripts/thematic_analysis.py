# thematic_analysis.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def load_data(filepath):
    return pd.read_csv(filepath)

def extract_keywords(df, max_features=50):
    tfidf = TfidfVectorizer(ngram_range=(1,2), max_features=max_features, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['review'].astype(str))
    keywords = tfidf.get_feature_names_out()
    return keywords

def assign_theme(text):
    text = text.lower()
    if any(kw in text for kw in ["login", "sign in", "authentication"]):
        return "Login Issues"
    elif any(kw in text for kw in ["slow", "lag", "not load", "freeze", "crash"]):
        return "Performance"
    elif any(kw in text for kw in ["interface", "ui", "design", "layout"]):
        return "UI/UX"
    elif any(kw in text for kw in ["feature", "add", "include", "tool"]):
        return "Feature Requests"
    elif any(kw in text for kw in ["support", "help", "customer"]):
        return "Customer Support"
    else:
        return "Other"

def add_theme_column(df):
    df['theme'] = df['review'].apply(assign_theme)
    return df

def save_keywords(keywords, path="keywords.csv"):
    pd.DataFrame(keywords, columns=["keyword"]).to_csv(path, index=False)
    print(f"Saved keywords to {path}")

def save_results(df, path="sentiment_results.csv"):
    df.to_csv(path, index=False)
    print(f"Updated file with themes saved to {path}")

if __name__ == "__main__":
    input_file = "sentiment_results.csv"
    df = load_data(input_file)
    
    keywords = extract_keywords(df)
    save_keywords(keywords)

    df = add_theme_column(df)
    save_results(df)
