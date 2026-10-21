# Mini Search Engine with RAG Extension

## Project Description

This project implements a mini search engine using classical Information Retrieval techniques and extends it with a simple Retrieval-Augmented Generation (RAG) component.

The system uses the Cranfield dataset and supports:

- Text preprocessing
- Inverted index construction
- TF computation
- IDF computation
- TF-IDF weighting
- Cosine similarity ranking
- Top-k document retrieval
- MAP evaluation
- NDCG@10 evaluation
- RAG-style answer generation from retrieved documents

---

## Dataset

The project uses the Cranfield dataset.

Required files should be placed inside the `data` folder:

```text
data/
├── cran.all.1400
├── cran.qry
├── cran.qrel
└── cranqrel.readme
```

The document collection contains 1400 documents.

Each document contains title and abstract fields. In this project, the document content used for indexing is:

```text
title + abstract
```

---

## Project Structure

```text
mini-search-engine-rag/
│
├── data/
│   ├── cran.all.1400
│   ├── cran.qry
│   ├── cran.qrel
│   └── cranqrel.readme
│
├── src/
│   ├── main.py
│   ├── parser.py
│   ├── preprocessing.py
│   ├── indexer.py
│   ├── ranking.py
│   ├── evaluation.py
│   └── rag.py
│
├── outputs/
│   └── sample_results.txt
│
├── report/
├── presentation/
└── README.md
```

---

## File Descriptions

### parser.py

This file parses the Cranfield dataset files and converts them into Python dictionaries.

It reads:

- `cran.all.1400`
- `cran.qry`
- `cran.qrel`

---

### preprocessing.py

This file performs text preprocessing.

The preprocessing steps are:

1. Lowercasing
2. Tokenization
3. Removing non-alphabetic tokens
4. Stopword removal
5. Stemming using Porter Stemmer

The same preprocessing function is applied to both documents and queries.

---

### indexer.py

This file builds the indexing and weighting components:

- Inverted index
- Term Frequency
- Inverse Document Frequency
- TF-IDF document vectors

---

### ranking.py

This file ranks documents for a given query using cosine similarity.

It includes:

- Query preprocessing
- Query TF-IDF vector creation
- Cosine similarity calculation
- Top-k document retrieval

---

### evaluation.py

This file evaluates the retrieval system using:

- MAP
- NDCG@10

---

### rag.py

This file implements a simple RAG-style answer generator.

It uses the top retrieved documents as context and generates a natural-language answer based on retrieved document snippets.

---

### main.py

This is the main file used to run the full system.

It performs the following steps:

1. Parse the dataset
2. Preprocess documents and queries
3. Build the inverted index
4. Compute TF, IDF, and TF-IDF
5. Rank documents using cosine similarity
6. Evaluate the system using MAP and NDCG@10
7. Generate a RAG-style answer
8. Save the results in `outputs/sample_results.txt`

---

## Requirements

This project requires Python and the NLTK library.

Install NLTK using:

```bash
pip install nltk
```

Download the required stopwords data once:

```bash
python -c "import nltk; nltk.download('stopwords')"
```

---

## How to Run the Project

### Using PyCharm

1. Open the project folder in PyCharm.
2. Make sure the Cranfield dataset files are inside the `data` folder.
3. Open:

```text
src/main.py
```

4. Right click inside the file.
5. Choose:

```text
Run 'main'
```

---

### Using Terminal

From the main project folder, run:

```bash
python src/main.py
```

---

## Evaluation Method

### MAP

MAP is calculated using binary relevance.

The Cranfield relevance scores are treated as follows:

| Cranfield Score | Binary Relevance |
|---|---|
| 1 | Relevant |
| 2 | Relevant |
| 3 | Relevant |
| 4 | Relevant |
| -1 or missing | Non-relevant |

---

### NDCG@10

NDCG@10 is calculated using graded relevance.

The Cranfield relevance scale is reversed, so the relevance scores are converted as follows:

| Original Relevance | Converted Relevance |
|---|---|
| 1 | 4 |
| 2 | 3 |
| 3 | 2 |
| 4 | 1 |
| -1 or missing | 0 |

---

## Sample Evaluation Results

Example results from the implemented system:

```text
MAP: 0.0071
NDCG@10: 0.0097
```

---

## Sample Query

```text
what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft.
```

---

## Sample Top Retrieved Documents

Example top retrieved documents for Query ID 1:

| Rank | Document ID | Score | Relevance |
|---|---:|---:|---:|
| 1 | 51 | 0.2744 | 3 |
| 2 | 184 | 0.2573 | 2 |
| 3 | 746 | 0.2363 | -1 |
| 4 | 12 | 0.2083 | 3 |
| 5 | 359 | 0.2063 | -1 |

---

## RAG Extension

The RAG component uses the top retrieved documents as context.

The process is:

1. The user query is processed.
2. The classical search engine retrieves the top-k documents.
3. The retrieved documents are passed to the RAG component.
4. The system generates a natural-language answer based on the retrieved documents.

This combines classical Information Retrieval with answer generation.

---

## Output File

After running the project, the generated results are saved in:

```text
outputs/sample_results.txt
```

This file includes:

- Dataset statistics
- MAP score
- NDCG@10 score
- Sample query
- Top retrieved documents
- RAG-generated answer

---

## Notes

- The same preprocessing steps are applied to both documents and queries.
- Documents not listed in `cran.qrel` are considered non-relevant.
- The Cranfield relevance scale is reversed, where score `1` represents the highest relevance.
- The RAG implementation in this project is a simple generator based on retrieved document snippets.