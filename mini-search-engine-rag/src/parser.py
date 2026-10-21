def parse_documents(file_path):
    """
    Parse cran.all.1400 file.
    Returns a dictionary:
    {
        doc_id: "title abstract"
    }
    """
    documents = {}

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    raw_docs = content.split(".I ")

    for raw_doc in raw_docs:
        raw_doc = raw_doc.strip()

        if not raw_doc:
            continue

        lines = raw_doc.splitlines()
        doc_id = int(lines[0].strip())

        title = ""
        abstract = ""
        current_section = None

        for line in lines[1:]:
            line = line.strip()

            if line == ".T":
                current_section = "title"
                continue
            elif line == ".A":
                current_section = "author"
                continue
            elif line == ".B":
                current_section = "bibliography"
                continue
            elif line == ".W":
                current_section = "abstract"
                continue

            if current_section == "title":
                title += line + " "
            elif current_section == "abstract":
                abstract += line + " "

        documents[doc_id] = (title + " " + abstract).strip()

    return documents


def parse_queries(file_path):
    """
    Parse cran.qry file.
    Returns a dictionary:
    {
        query_id: "query text"
    }
    """
    queries = {}

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    raw_queries = content.split(".I ")

    for raw_query in raw_queries:
        raw_query = raw_query.strip()

        if not raw_query:
            continue

        lines = raw_query.splitlines()
        query_id = int(lines[0].strip())

        query_text = ""
        current_section = None

        for line in lines[1:]:
            line = line.strip()

            if line == ".W":
                current_section = "query"
                continue

            if current_section == "query":
                query_text += line + " "

        queries[query_id] = query_text.strip()

    return queries


def parse_qrels(file_path):
    """
    Parse cran.qrel file.
    Returns a dictionary:
    {
        query_id: {
            doc_id: relevance_score
        }
    }
    """
    qrels = {}

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            parts = line.strip().split()

            if len(parts) < 3:
                continue

            query_id = int(parts[0])
            doc_id = int(parts[1])
            relevance = int(parts[2])

            if query_id not in qrels:
                qrels[query_id] = {}

            qrels[query_id][doc_id] = relevance

    return qrels