from collections import defaultdict, Counter
import math
from preprocessing import preprocess_text


def build_inverted_index(documents):
    """
    Build an inverted index.

    Returns:
    {
        term: set(doc_ids)
    }
    """
    inverted_index = defaultdict(set)

    for doc_id, text in documents.items():
        tokens = preprocess_text(text)

        for token in tokens:
            inverted_index[token].add(doc_id)

    return inverted_index


def compute_tf(documents):
    """
    Compute term frequency for each document.

    Returns:
    {
        doc_id: {
            term: frequency
        }
    }
    """
    tf = {}

    for doc_id, text in documents.items():
        tokens = preprocess_text(text)
        tf[doc_id] = dict(Counter(tokens))

    return tf


def compute_idf(documents, inverted_index):
    """
    Compute inverse document frequency for each term.

    IDF = log(N / df)

    Returns:
    {
        term: idf_value
    }
    """
    idf = {}
    total_documents = len(documents)

    for term, doc_ids in inverted_index.items():
        document_frequency = len(doc_ids)
        idf[term] = math.log(total_documents / document_frequency)

    return idf


def compute_tfidf(tf, idf):
    """
    Compute TF-IDF vectors for all documents.

    Returns:
    {
        doc_id: {
            term: tfidf_weight
        }
    }
    """
    tfidf = {}

    for doc_id, term_freqs in tf.items():
        tfidf[doc_id] = {}

        for term, freq in term_freqs.items():
            tfidf[doc_id][term] = freq * idf.get(term, 0)

    return tfidf