from pathlib import Path

from parser import parse_documents, parse_queries, parse_qrels
from indexer import (
    build_inverted_index,
    compute_tf,
    compute_idf,
    compute_tfidf
)
from ranking import rank_documents
from evaluation import mean_average_precision, mean_ndcg
from rag import generate_rag_answer


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"

OUTPUTS_DIR.mkdir(exist_ok=True)


def main():
    documents = parse_documents(DATA_DIR / "cran.all.1400")
    queries = parse_queries(DATA_DIR / "cran.qry")
    qrels = parse_qrels(DATA_DIR / "cran.qrel")

    print("Building index...")

    inverted_index = build_inverted_index(documents)
    tf = compute_tf(documents)
    idf = compute_idf(documents, inverted_index)
    tfidf = compute_tfidf(tf, idf)

    print("Ranking documents for all queries...")

    all_ranked_results = {}

    for query_id, query_text in queries.items():
        ranked_results = rank_documents(query_text, tfidf, idf, top_k=100)
        all_ranked_results[query_id] = ranked_results

    print("Evaluating...")

    map_score = mean_average_precision(all_ranked_results, qrels)
    ndcg_score = mean_ndcg(all_ranked_results, qrels, k=10)

    sample_query_id = 1
    sample_query = queries[sample_query_id]
    sample_results = all_ranked_results[sample_query_id]

    rag_answer = generate_rag_answer(
        sample_query,
        sample_results,
        documents,
        max_docs=3
    )

    output_text = ""

    output_text += "Mini Search Engine with RAG Extension\n"
    output_text += "=====================================\n\n"

    output_text += "Dataset Statistics\n"
    output_text += "------------------\n"
    output_text += f"Number of documents: {len(documents)}\n"
    output_text += f"Number of queries: {len(queries)}\n"
    output_text += f"Number of qrels: {len(qrels)}\n"
    output_text += f"Number of unique terms: {len(inverted_index)}\n\n"

    output_text += "Evaluation Results\n"
    output_text += "------------------\n"
    output_text += f"MAP: {map_score:.4f}\n"
    output_text += f"NDCG@10: {ndcg_score:.4f}\n\n"

    output_text += "Sample Query\n"
    output_text += "------------\n"
    output_text += f"Query ID: {sample_query_id}\n"
    output_text += f"Query: {sample_query}\n\n"

    output_text += "Top 5 Retrieved Documents\n"
    output_text += "-------------------------\n"

    for rank, (doc_id, score) in enumerate(sample_results[:5], start=1):
        relevance = qrels.get(sample_query_id, {}).get(doc_id, -1)

        output_text += (
            f"{rank}. Doc {doc_id} | "
            f"Score: {score:.4f} | "
            f"Relevance: {relevance}\n"
        )
        output_text += documents[doc_id][:300] + "\n\n"

    output_text += "RAG Generated Answer\n"
    output_text += "--------------------\n"
    output_text += rag_answer + "\n"

    print()
    print(output_text)

    output_file = OUTPUTS_DIR / "sample_results.txt"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(output_text)

    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()