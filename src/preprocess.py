import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_data(csv_path):
    """
    Loads dataset and converts email text into TF-IDF features.
    """

    df = pd.read_csv(csv_path)

    # Basic validation
    if "email_text" not in df.columns or "label" not in df.columns:
        raise ValueError("Dataset must contain 'email_text' and 'label' columns")

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df["email_text"])
    y = df["label"]

    return X, y, vectorizer
