# RAG Pipeline Project

This project implements a complete Retrieval-Augmented Generation (RAG) pipeline in Python, consisting of document ingestion, semantic retrieval, and answer generation using retrieved context.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate

pip install pypdf
pip install sentence-transformers
pip install faiss-cpu
pip install transformers
pip install torch
```

## Module 1: Document Ingestion (`ingest.py`)

Loads PDF/TXT documents, extracts and cleans text, creates configurable chunks, adds metadata (source, page, chunk_id), and exports the results to `chunks.json`.

Run:

```bash
python ingest.py
```

Custom chunking:

```bash
python ingest.py --chunk-size 300 --overlap 30
```

---

## Module 2: Semantic Retrieval (`retrieval.py`)

Generates embeddings using Sentence Transformers, indexes all chunks in FAISS, and performs semantic search with configurable `top_k`.

Run:

```bash
python retrieval.py
```

Output:

```text
vector.index
```

---

## Module 3: End-to-End RAG (`rag.py`)

Accepts a user question, retrieves relevant chunks from the vector store, generates an answer using only the retrieved context, and returns the supporting sources.

Run:

```bash
python rag.py
```

Example:

```text
Question: What is machine learning?

Answer:
a subset of artificial intelligence

Sources:
ai_notes.txt
```
If information is not found:

```text
Question: What is the CEO salary?

Answer:
I cannot find enough evidence in the provided documents.

Citation:
None
```

## Module 4: Evaluation & Enhancement (`evaluation.md`)

Improves retrieval using **Query Rewriting** and adds **citations** to generated answers.

Features:
- Query rewriting (e.g., AI → Artificial Intelligence)
- Source citations
- Evaluation set of 10 questions
- Grounded answer validation

Result: **10/10 evaluation score**

---

## Project Structure

```text
rag-ingestion/
├── documents/
├── ingest.py
├── retrieval.py
├── rag.py
├── evaluation.md
├── chunks.json
├── vector.index
├── README.md
└── .gitignore
```


## Workflow

```text
Documents
    ↓
Ingestion
    ↓
Chunks + Metadata
    ↓
Embeddings + FAISS
    ↓
Semantic Retrieval
    ↓
LLM
    ↓
Answer + Sources
```

## Features

✅ Load and process PDF/TXT documents  
✅ Configurable chunk size and overlap  
✅ Metadata included for every chunk  
✅ Embedding generation and vector indexing  
✅ Semantic similarity search  
✅ Grounded answer generation  
✅ Source attribution  
✅ No-evidence fallback response