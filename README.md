# RAG Pipeline Project

This project implements a complete Retrieval-Augmented Generation (RAG) pipeline in Python, consisting of document ingestion, semantic retrieval, answer generation, workflow orchestration with LangGraph, and multi-tool agent capabilities.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate

pip install pypdf
pip install sentence-transformers
pip install faiss-cpu
pip install transformers
pip install torch
pip install langgraph
pip install langchain-core
```

---

## Module 1: Document Ingestion (`ingest.py`)

Loads PDF/TXT documents, extracts and cleans text, creates configurable chunks, adds metadata (source, page, chunk_id), and exports the results to `chunks.json`.

Run:

```bash
python ingest.py
```

Custom chunking:

```bash
python ingest.py --chunk-size 500 --overlap 50
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

Accepts a user question, retrieves relevant chunks from the vector store, generates an answer using only the retrieved context, and returns citations.

Run:

```bash
python rag.py
```

Example:

```text
Question: What is machine learning?

Answer:
a subset of artificial intelligence

Citation:
ai_notes.txt
```

Unsupported question:

```text
Question: What is the CEO salary?

Answer:
I cannot find enough evidence in the provided documents.

Citation:
None
```

---

## Module 4: Evaluation & Enhancement (`evaluation.md`)

Improves retrieval using Query Rewriting and adds citations to generated answers.

Features:

- Query rewriting (AI → Artificial Intelligence)
- Source citations
- Evaluation set of 10 questions
- Grounded answer validation

Result: **10/10 evaluation score**

---

## Module 5: RAG Knowledge Assistant

Combines all previous modules into a complete document Question & Answer assistant.

### Architecture

```text
User Question
      ↓
RAG Assistant
      ↓
Knowledge Base
      ↓
Answer + Citation
```

Outcome:

- Answers questions from documents
- Returns citations
- Handles unsupported questions safely

---

## Module 6: LangGraph Orchestration (`graph.py`)

Wraps the RAG workflow in a LangGraph state machine with explicit state, nodes, and edges.

### Architecture

```text
Question
    ↓
Rewrite Node
    ↓
Retrieve Node
    ↓
Generate Node
    ↓
Output Node
```

Features:

- Explicit state schema
- Graph-based workflow
- State logging
- Retrieval and generation as graph nodes

Run:

```bash
python graph.py
```

---

## Module 7: Multi-Tool Agent (`graph.py`)

Extends the LangGraph workflow with additional tools and intelligent routing.

### Available Tools

- RAG Knowledge Base
- Calculator Tool
- Customer Lookup Tool

### Architecture

```text
                 Router
                    │
     ┌──────────────┼──────────────┐
     ↓              ↓              ↓
 Calculator     Customer          RAG
     │              │              │
     └──────────────┴──────────────┘
                    ↓
                 Output
```

Example:

```text
Question: 25 * 4

Answer:
Result = 100
```

```text
Question: customer 1001

Answer:
Customer: John Smith | Status: Active
```

---

## Project Structure

```text
rag-ingestion/
├── documents/
├── ingest.py
├── retrieval.py
├── rag.py
├── graph.py
├── evaluation.md
├── chunks.json
├── vector.index
├── README.md
└── .gitignore
```

---

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
Query Rewriting
    ↓
Semantic Retrieval
    ↓
LLM
    ↓
LangGraph Workflow
    ↓
Multi-Tool Agent
    ↓
Answer + Citation
```

---

## Features

✅ Document ingestion and chunking  
✅ Metadata generation  
✅ Sentence Transformer embeddings  
✅ FAISS vector search  
✅ Query rewriting  
✅ Grounded answer generation  
✅ Source citations  
✅ Safe failure handling  
✅ LangGraph orchestration  
✅ Multi-tool agent routing  
✅ Calculator tool  
✅ Customer lookup tool  
✅ Evaluation dataset and testing