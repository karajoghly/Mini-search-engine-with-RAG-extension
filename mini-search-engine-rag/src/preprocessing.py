import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))


def preprocess_text(text):
    """
    Preprocess text using:
    1. Lowercasing
    2. Tokenization
    3. Removing non-alphabetic tokens
    4. Stopword removal
    5. Stemming

    Returns a list of processed tokens.
    """
    text = text.lower()

    # Keep only English alphabetic words
    tokens = re.findall(r"[a-z]+", text)

    processed_tokens = []

    for token in tokens:
        if token not in stop_words:
            stemmed_token = stemmer.stem(token)
            processed_tokens.append(stemmed_token)

    return processed_tokens