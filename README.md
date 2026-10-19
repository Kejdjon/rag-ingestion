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
## Module 9: MCP Integration

An MCP server was integrated with the LangGraph agent to provide employee lookup functionality.

### Start MCP Server

```bash
mcp run mcp_server.py --transport streamable-http
```

### Start Agent

```bash
python graph.py
```

### Example

Input:

```text
employee 1001
```

Output:

```text
John Smith - IT
```

### Failure Handling

If the MCP server is unavailable:

```text
MCP server unavailable
```

### Features

- MCP Server (`mcp_server.py`)
- MCP Client (`mcp_client.py`)
- Employee Lookup Tool
- LangGraph MCP Routing
- Graceful Error Handling

## Week 3: PDF Intake and Classification

A PDF intake pipeline was implemented to analyze uploaded PDF documents and determine the appropriate extraction strategy.

### Features

- PDF validation and intake
- Metadata extraction (file name and page count)
- Text-based PDF detection
- Scanned PDF detection
- Processing-path selection
- Classification logging
- CSV output generation

### Processing Flow

```text
PDF Upload
     ↓
Metadata Extraction
     ↓
Document Classification
     ↓
 ┌───────────────┬───────────────┐
 ↓                               ↓
Text-Based PDF            Scanned PDF
 ↓                               ↓
Direct Extraction           OCR Required
```

### Classification Results

| Document | Classification | Processing |
|-----------|---------------|------------|
| Introduction to Artificial Intelligence.pdf | Text-Based | Direct Text Extraction |
| Employee Handbook.pdf | Text-Based | Direct Text Extraction |
| EMPLOYEE APPLICATION FORM.pdf | Scanned | OCR Required |
| INVOICE.pdf | Scanned | OCR Required |
| Doc6.pdf | Scanned | OCR Required |

### Run

```bash
python intake.py
```

### Output

The intake module generates:

```text
classification_results.csv
```

containing:

- File name
- Status
- Page count
- Classification
- Processing decision

### Outcome

The solution successfully identifies whether a PDF should be processed through direct text extraction or OCR and logs the selected processing path for downstream document extraction workflows.
## Week 3: OCR Processing

An OCR module was implemented to process scanned PDF documents identified during intake classification.

### Features

- OCR extraction using Tesseract
- Page-level OCR output
- Text normalization
- Quality assessment
- Controlled error handling

### Workflow

```text
Scanned PDF
     ↓
PDF to Image Conversion
     ↓
OCR Extraction
     ↓
Text Normalization
     ↓
Quality Check
     ↓
Structured Output
```

### Example Results

#### INVOICE.pdf

```text
Page: 1
Quality: OK

INVOICE
Invoice Number: INV-1001
Customer: ABC Trading Ltd
Amount Due: EUR 2,500
```

#### EMPLOYEE APPLICATION FORM.pdf

```text
Page: 1
Quality: OK

EMPLOYEE APPLICATION FORM
First Name:
Last Name:
Department:
Phone Number:
Email Address:
Signature:
```

### Outcome

The OCR module successfully extracts text from scanned PDFs, normalizes the output, flags low-quality pages, and returns controlled status messages when processing fails. The extracted text is prepared for downstream structured extraction and comparison activities.


## Week 3: Document Intelligence Style Processing

### PDF Intake & Classification
- Detects text-based vs scanned PDFs
- Extracts metadata
- Routes documents to extraction or OCR

### OCR Processing
- Tesseract OCR
- Text normalization
- Quality flags
- Error handling

### Document Intelligence Processing
- Structured JSON output
- Page references
- Source references
- Key-value extraction
- OCR vs DI comparison
## Week 3: Extract Validated Business Fields

The final stage of the document-processing workflow transforms extracted document content into validated business data using Pydantic schemas.

### Objective

Convert unstructured document content into structured, application-ready JSON objects while ensuring data validation and traceability.

### Technologies Used

- Python
- Pydantic
- JSON
- OCR Output
- Structured Document Extraction

### Invoice Schema

The invoice model includes the following business fields:

- Invoice Number
- Customer
- Invoice Date
- Amount Due
- Services Provided
- Source Document
- Page Number

### Extraction Pipeline

```text
PDF
 ↓
OCR Processing
 ↓
Structured Document Output
 ↓
Business Field Extraction
 ↓
Pydantic Validation
 ↓
JSON Business Object
```

### Features

- Strongly typed business schema
- Structured JSON output
- Null handling for missing information
- Validation and fallback logic
- Source traceability
- Page-level evidence retention

### Example Output

```json
{
  "invoice_number": "INV-1001",
  "customer": "ABC Trading Ltd",
  "invoice_date": "12 October 2026",
  "amount_due": "EUR 2,500",
  "services_provided": "Consulting Services",
  "source_document": "INVOICE.pdf",
  "page_number": 1
}
```

### Missing Data Handling

Documents that do not contain invoice information return null values instead of generating or inventing data.

Example:

```json
{
  "invoice_number": null,
  "customer": null,
  "invoice_date": null,
  "amount_due": null,
  "services_provided": null,
  "source_document": "Employee Handbook.pdf",
  "page_number": 1
}
```

### Validation Strategy

If extraction or validation fails:

- Missing values are returned as `null`
- Source information is preserved
- Processing continues without application failure

### Outcome

The solution converts OCR and structured document output into validated business objects that can be consumed by downstream applications, APIs, databases, or analytics workflows. By using Pydantic validation, data quality and consistency are maintained while preserving document source and page references for auditing and traceability.