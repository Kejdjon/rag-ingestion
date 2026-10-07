# RAG Pipeline Project

This project implements a complete Retrieval-Augmented Generation (RAG) pipeline in Python consisting of document ingestion, semantic retrieval, answer generation, LangGraph orchestration, multi-tool routing, and error recovery.

---

# Installation

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

# Module 1: Document Ingestion (`ingest.py`)

Loads PDF/TXT documents, extracts and cleans text, creates configurable chunks, adds metadata, and exports the results to `chunks.json`.

## Features

- PDF and TXT document support
- Text cleaning
- Configurable chunk size
- Configurable overlap
- Metadata generation

Metadata includes:

```json
{
  "source": "ai_notes.txt",
  "page": 1,
  "chunk_id": 0
}
```

## Run

```bash
python ingest.py
```

Custom chunking:

```bash
python ingest.py --chunk-size 500 --overlap 50
```

## Output

```text
chunks.json
```

---

# Module 2: Semantic Retrieval (`retrieval.py`)

Generates embeddings using Sentence Transformers and indexes document chunks using FAISS for semantic search.

## Technologies

### Embedding Model

```text
all-MiniLM-L6-v2
```

### Vector Database

```text
FAISS
```

## Workflow

```text
Chunks
   ↓
Embeddings
   ↓
FAISS Index
   ↓
Semantic Search
```

## Run

```bash
python retrieval.py
```

## Output

```text
vector.index
```

---

# Module 3: End-to-End RAG (`rag.py`)

Combines retrieval and generation to answer user questions using retrieved document context.

## Features

- Query Rewriting
- Semantic Retrieval
- FLAN-T5 Generation
- Source Citations
- Safe Failure Handling

## Run

```bash
python rag.py
```

## Example

```text
Question:
What is machine learning?

Answer:
a subset of artificial intelligence

Citation:
ai_notes.txt
```

## Unsupported Question

```text
Question:
What is the CEO salary?

Answer:
I cannot find enough evidence in the provided documents.

Citation:
None
```

---

# Module 4: Evaluation & Enhancement (`evaluation.md`)

Improves retrieval quality and validates solution performance.

## Enhancements

- Query Rewriting
- Citation Support
- Grounded Answer Verification

Examples:

```text
AI → Artificial Intelligence

Staff → Employees

ML → Machine Learning
```

## Results

```text
10 Questions Tested
10 Correct Results
Score: 10/10
```

---

# Module 5: RAG Knowledge Assistant

Combines the ingestion, retrieval, and generation modules into a complete document Question & Answer assistant.

## Architecture

```text
User Question
      ↓
RAG Assistant
      ↓
Knowledge Base
      ↓
Answer + Citation
```

## Features

✅ Answers questions from documents

✅ Returns citations

✅ Reduces hallucinations

✅ Safe fallback for unsupported questions

---

# Module 6: LangGraph Orchestration (`graph.py`)

Wraps the RAG workflow into a LangGraph state machine.

## State Schema

```python
class AgentState(TypedDict):
    question: str
    tool: str
    rewritten_question: str
    context: str
    answer: str
    citation: str
    score: float
    status: str
```

The state acts as shared memory between all graph nodes.

## Graph Architecture

```text
Question
    ↓
Rewrite
    ↓
Retrieve
    ↓
Generate
    ↓
Output
```

## LangGraph Components

### Nodes

- Rewrite Node
- Retrieve Node
- Generate Node
- Output Node

### Edges

```text
Rewrite
   ↓
Retrieve
   ↓
Generate
   ↓
Output
```

### Shared State

Stores:

```text
Question
Context
Answer
Citation
Score
```

---

# Module 7: Multi-Tool Agent (`graph.py`)

Extends the LangGraph workflow with multiple capabilities.

## Available Tools

### RAG Knowledge Assistant

Used for document-based questions.

Example:

```text
What is machine learning?
```

---

### Calculator Tool

Used for mathematical calculations.

Example:

```text
25 * 4
```

Output:

```text
Result = 100
```

---

### Customer Lookup Tool

Uses a mock customer database.

Example:

```text
customer 1001
```

Output:

```text
Customer: John Smith | Status: Active
```

---

# Module 8: Routing & Recovery (`graph.py`)

Adds intelligent routing, structured outputs, and graceful failure handling.

## Router Node

Routes questions to the correct capability.

```text
User Question
      ↓
Router
      ↓
 ┌────┼────┐
 ↓    ↓    ↓
RAG Calc Customer
```

### Routing Examples

```text
What is AI?
→ RAG
```

```text
25 * 4
→ Calculator
```

```text
customer 1001
→ Customer Lookup
```

---

## Conditional Routing

Implemented with LangGraph conditional edges.

```python
graph_builder.add_conditional_edges(...)
```

This dynamically selects the workflow path.

---

## Structured Output

All nodes return a consistent response structure:

```python
{
    "status": "success",
    "answer": "...",
    "citation": "..."
}
```

Error responses:

```python
{
    "status": "error",
    "answer": "...",
    "citation": "..."
}
```

---

## Error Recovery

The agent handles failures without crashing.

### Calculator Error

Input:

```text
25**
```

Output:

```text
Invalid mathematical expression.
```

---

### Customer Error

Input:

```text
customer 9999
```

Output:

```text
Customer not found
```

---

### Unsupported RAG Question

Input:

```text
What is CEO salary?
```

Output:

```text
I cannot find enough evidence in the provided documents.
```

---

# Project Structure

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

# End-to-End Architecture

```text
Documents
    ↓
Ingestion
    ↓
Chunks + Metadata
    ↓
Embeddings
    ↓
FAISS
    ↓
Semantic Retrieval
    ↓
FLAN-T5
    ↓
LangGraph
    ↓
Router
 ┌──┼──┐
 ↓  ↓  ↓
RAG Calc Customer
    ↓
Answer + Citation
```

---

# Example Questions

## RAG

```text
What is AI?
```

```text
What is machine learning?
```

---

## Calculator

```text
25 * 4
```

```text
100 / 5
```

---

## Customer Lookup

```text
customer 1001
```

```text
customer 1002
```

---

## Error Recovery

```text
25**
```

```text
customer 9999
```

```text
What is CEO salary?
```

---

# Features

✅ PDF/TXT ingestion

✅ Configurable chunking

✅ Metadata generation

✅ Sentence Transformer embeddings

✅ FAISS vector search

✅ FLAN-T5 generation

✅ Query rewriting

✅ Source citations

✅ Safe fallback handling

✅ LangGraph orchestration

✅ Shared state management

✅ Conditional routing

✅ Multi-tool agent

✅ Calculator tool

✅ Customer lookup tool

✅ Error recovery

✅ Structured outputs

✅ Evaluation framework

✅ End-to-end RAG workflow