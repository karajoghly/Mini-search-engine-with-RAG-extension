import math


def is_relevant(qrels, query_id, doc_id):
    """
    Binary relevance for MAP.
    Scores 1, 2, 3, 4 are relevant.
    Missing or -1 is non-relevant.
    """
    relevance = qrels.get(query_id, {}).get(doc_id, -1)
    return relevance in [1, 2, 3, 4]


def convert_to_graded_relevance(original_relevance):
    """
    Cranfield relevance scale is reversed:
    1 -> 4
    2 -> 3
    3 -> 2
    4 -> 1
    -1 or missing -> 0
    """
    mapping = {
        1: 4,
        2: 3,
        3: 2,
        4: 1
    }

    return mapping.get(original_relevance, 0)


def average_precision(ranked_results, qrels, query_id):
    """
    Compute Average Precision for one query.
    """
    relevant_count = 0
    precision_sum = 0

    total_relevant = sum(
        1 for relevance in qrels.get(query_id, {}).values()
        if relevance in [1, 2, 3, 4]
    )

    if total_relevant == 0:
        return 0

    for rank, (doc_id, score) in enumerate(ranked_results, start=1):
        if is_relevant(qrels, query_id, doc_id):
            relevant_count += 1
            precision_at_rank = relevant_count / rank
            precision_sum += precision_at_rank

    return precision_sum / total_relevant


def mean_average_precision(all_ranked_results, qrels):
    """
    Compute MAP over all queries.

    all_ranked_results:
    {
        query_id: [(doc_id, score), ...]
    }
    """
    ap_scores = []

    for query_id, ranked_results in all_ranked_results.items():
        ap = average_precision(ranked_results, qrels, query_id)
        ap_scores.append(ap)

    if not ap_scores:
        return 0

    return sum(ap_scores) / len(ap_scores)


def dcg(ranked_results, qrels, query_id, k=10):
    """
    Compute DCG@k for one query.
    """
    score = 0

    for rank, (doc_id, _) in enumerate(ranked_results[:k], start=1):
        original_relevance = qrels.get(query_id, {}).get(doc_id, -1)
        relevance = convert_to_graded_relevance(original_relevance)

        score += relevance / math.log2(rank + 1)

    return score


def ideal_dcg(qrels, query_id, k=10):
    """
    Compute ideal DCG@k for one query.
    """
    relevances = []

    for original_relevance in qrels.get(query_id, {}).values():
        relevances.append(convert_to_graded_relevance(original_relevance))

    relevances.sort(reverse=True)

    score = 0

    for rank, relevance in enumerate(relevances[:k], start=1):
        score += relevance / math.log2(rank + 1)

    return score


def ndcg(ranked_results, qrels, query_id, k=10):
    """
    Compute NDCG@k for one query.
    """
    actual_dcg = dcg(ranked_results, qrels, query_id, k)
    ideal = ideal_dcg(qrels, query_id, k)

    if ideal == 0:
        return 0

    return actual_dcg / ideal


def mean_ndcg(all_ranked_results, qrels, k=10):
    """
    Compute mean NDCG@k over all queries.
    """
    ndcg_scores = []

    for query_id, ranked_results in all_ranked_results.items():
        score = ndcg(ranked_results, qrels, query_id, k)
        ndcg_scores.append(score)

    if not ndcg_scores:
        return 0

    return sum(ndcg_scores) / len(ndcg_scores)