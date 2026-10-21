import math
from collections import Counter
from preprocessing import preprocess_text


def compute_query_vector(query, idf):
    """
    Convert a query into a TF-IDF vector using the existing IDF values.
    """
    tokens = preprocess_text(query)
    query_tf = Counter(tokens)

    query_vector = {}

    for term, freq in query_tf.items():
        if term in idf:
            query_vector[term] = freq * idf[term]

    return query_vector


def cosine_similarity(vector1, vector2):
    """
    Compute cosine similarity between two sparse vectors represented as dictionaries.
    """
    dot_product = 0

    for term, weight in vector1.items():
        dot_product += weight * vector2.get(term, 0)

    magnitude1 = math.sqrt(sum(weight ** 2 for weight in vector1.values()))
    magnitude2 = math.sqrt(sum(weight ** 2 for weight in vector2.values()))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    return dot_product / (magnitude1 * magnitude2)


def rank_documents(query, documents_tfidf, idf, top_k=10):
    """
    Rank documents for a given query using cosine similarity.

    Returns:
    [
        (doc_id, score),
        ...
    ]
    """
    query_vector = compute_query_vector(query, idf)

    scores = []

    for doc_id, doc_vector in documents_tfidf.items():
        score = cosine_similarity(query_vector, doc_vector)

        if score > 0:
            scores.append((doc_id, score))

    scores.sort(key=lambda item: item[1], reverse=True)

    return scores[:top_k]