def generate_rag_answer(query, top_results, documents, max_docs=3):
    """
    Simple RAG-style answer generator.

    It takes the top retrieved documents and creates a natural-language
    answer based on their content.
    """
    selected_docs = top_results[:max_docs]

    if not selected_docs:
        return "No relevant documents were found for this query."

    answer = "Based on the retrieved documents, the answer can be summarized as follows:\n\n"

    for rank, (doc_id, score) in enumerate(selected_docs, start=1):
        document_text = documents[doc_id]

        # Take a short part of each retrieved document
        snippet = document_text[:500].strip()

        answer += f"Document {doc_id} discusses: {snippet}\n\n"

    answer += (
        "Overall, these documents provide information related to the query "
        "and can be used as supporting evidence for the generated answer."
    )

    return answer