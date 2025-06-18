import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load preprocessed sentiment-labeled reviews
df = pd.read_csv("../data/analyzed/sentiment_results.csv")  # Adjust path as needed

# Handle missing or non-string review values safely
df['review'] = df['review'].fillna('').astype(str)


# --- THEME ASSIGNMENT FUNCTION ---
def assign_theme(text):
    if not isinstance(text, str):
        return 'unknown'
    
    text = text.lower()

    if any(keyword in text for keyword in ['login', 'password', 'sign in']):
        return 'Login Issues'
    elif any(keyword in text for keyword in ['slow', 'lag', 'load', 'freeze']):
        return 'Performance & Speed'
    elif any(keyword in text for keyword in ['crash', 'bug', 'error', 'glitch']):
        return 'Stability & Reliability'
    elif any(keyword in text for keyword in ['fingerprint', 'feature', 'option', 'function']):
        return 'Feature Requests'
    elif any(keyword in text for keyword in ['support', 'help', 'service', 'agent']):
        return 'Customer Support'
    elif any(keyword in text for keyword in ['interface', 'ui', 'design', 'layout']):
        return 'UI/UX'
    else:
        return 'Other'


# Assign theme based on review text
df['theme'] = df['review'].apply(assign_theme)


# --- TF-IDF Keyword Extraction ---
vectorizer = TfidfVectorizer(stop_words='english', max_features=20)
X = vectorizer.fit_transform(df['review'])

# Save top keywords
keywords = vectorizer.get_feature_names_out()
keyword_df = pd.DataFrame(keywords, columns=['keyword'])
keyword_df.to_csv("../data/analyzed/keywords.csv", index=False)
print("✅ Saved top keywords to keywords.csv")


# Save updated dataset with theme
df.to_csv("../data/analyzed/themed_reviews.csv", index=False)
print("✅ Saved reviews with themes to themed_reviews.csv")
