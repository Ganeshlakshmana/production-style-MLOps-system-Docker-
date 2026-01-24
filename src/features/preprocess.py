from sklearn.feature_extraction.text import TfidfVectorizer

def fit_transform(texts):
    vec = TfidfVectorizer(max_features=5000, stop_words="english")
    X = vec.fit_transform(texts)
    return X, vec
