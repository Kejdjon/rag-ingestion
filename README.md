# AI Assistant Backend Project

## Overview

This project demonstrates the development of an AI-powered backend application across four weeks, covering Retrieval-Augmented Generation (RAG), agent-based workflows, document processing, API development, containerization, persistence, security, observability, and CI/CD.

The solution is implemented using Python, FastAPI, Docker, Pydantic, FAISS, LangGraph, GitHub Actions, and OCR technologies.

---

# Week 1 - Retrieval-Augmented Generation (RAG)

## Objective

Build a Retrieval-Augmented Generation (RAG) solution capable of answering user questions using uploaded documents instead of relying only on pre-trained model knowledge.

## Components Implemented

### Document Ingestion

A document ingestion pipeline was developed to load and process PDF and text documents.

Features:

- PDF document support
- Text document support
- Text extraction
- Metadata generation
- Pre-processing and cleaning

Metadata example:

```json
{
  "source": "ai_notes.txt",
  "page": 1,
  "chunk_id": 0
}
```

### Text Chunking

Large documents were divided into smaller overlapping chunks.

Benefits:

- Improved retrieval quality
- Better semantic matching
- Reduced context loss
- Faster vector indexing

### Embedding Generation

Document chunks were converted into vector embeddings using Sentence Transformers.

Embedding model:

```text
all-MiniLM-L6-v2
```

Features:

- Semantic understanding
- Similarity-based search
- Dense vector representations

### Vector Storage

Embeddings were indexed using FAISS.

Benefits:

- Fast retrieval
- Efficient similarity search
- Scalable vector storage

### Semantic Retrieval

When users submit a question:

1. The question is converted into an embedding.
2. FAISS performs similarity search.
3. Most relevant chunks are retrieved.
4. Context is passed to the generation model.

### Answer Generation

Retrieved context is combined with the user question to generate grounded answers.

Features:

- Retrieval-Augmented Generation
- Citation support
- Grounded answers
- Reduced hallucinations

### Query Enhancement

Implemented query rewriting to improve retrieval quality.

Examples:

```text
AI → Artificial Intelligence

ML → Machine Learning

Staff → Employees
```

### Safe Failure Handling

Unsupported questions return controlled responses.

Example:

```text
Question:
What is the CEO salary?

Answer:
I cannot find enough evidence in the provided documents.
```

### Architecture

```text
Documents
     ↓
Chunking
     ↓
Embeddings
     ↓
FAISS Index
     ↓
User Question
     ↓
Retriever
     ↓
Relevant Context
     ↓
Answer Generation
```

### Outcome

The Week 1 solution successfully implemented a complete RAG pipeline capable of retrieving relevant information from documents and generating evidence-based answers.

---

# Week 2 - LangGraph Agent & MCP Integration

## Objective

Extend the RAG solution into an intelligent agent capable of selecting different tools and workflows dynamically.

## LangGraph Orchestration

A LangGraph workflow was designed to coordinate multiple processing steps.

### Workflow

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

### Shared State

The workflow uses a shared state object containing:

```text
Question
Context
Answer
Citation
Score
Status
```

### Nodes

Implemented nodes:

- Rewrite Node
- Retrieve Node
- Generate Node
- Output Node

### Benefits

- Modular architecture
- State sharing
- Easier maintenance
- Workflow visibility

---

## Multi-Tool Agent

The LangGraph workflow was extended with multiple tools.

### RAG Knowledge Assistant

Used for knowledge-based questions.

Example:

```text
What is machine learning?
```

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

## Intelligent Routing

A router node was added to determine the correct processing path.

Workflow:

```text
User Question
      ↓
Router
      ↓
 ┌────┼────┐
 ↓    ↓    ↓
RAG Calc Customer
```

Routing examples:

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

## Error Recovery

The agent handles failures without crashing.

Examples:

### Calculator Error

```text
Input:
25**

Output:
Invalid mathematical expression.
```

### Missing Customer

```text
Input:
customer 9999

Output:
Customer not found.
```

### Unsupported Document Question

```text
Input:
What is CEO salary?

Output:
I cannot find enough evidence in the provided documents.
```

---

## MCP Integration

An MCP server was integrated to provide employee lookup capabilities.

### Components

- MCP Server
- MCP Client
- Employee Lookup Tool
- LangGraph MCP Routing

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

If MCP is unavailable:

```text
MCP server unavailable
```

### Outcome

The Week 2 solution introduced agent orchestration, intelligent routing, multi-tool support, and MCP integration while maintaining structured outputs and graceful failure handling.

---

# Week 3 - Document Processing & Extraction

## Objective

Build a complete document-processing pipeline capable of classifying documents, extracting text, performing OCR, and generating structured business data.

---

## PDF Intake & Classification

### Features

- PDF validation
- Metadata extraction
- Page counting
- Classification logic
- Processing path selection

### Workflow

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

### Classification Output

Generated:

```text
classification_results.csv
```

Containing:

- File Name
- Status
- Page Count
- Classification
- Processing Decision

### Outcome

Documents were automatically classified as text-based or scanned to determine the correct processing strategy.

---

## OCR Processing

### Features

- OCR extraction
- Page-level processing
- Text normalization
- Quality validation
- Controlled error handling

### Workflow

```text
Scanned PDF
     ↓
PDF to Image
     ↓
OCR
     ↓
Normalization
     ↓
Quality Check
```

### OCR Example

```text
INVOICE

Invoice Number: INV-1001
Customer: ABC Trading Ltd
Amount Due: EUR 2,500
```

### Benefits

- Recovery of text from scanned documents
- Structured OCR outputs
- Error resilience
- Page-level traceability

---

## Document Intelligence Style Processing

### Features

- Structured extraction
- Source tracking
- Page references
- OCR comparison
- Key-value extraction

Generated output includes:

```text
Source Document
Page Number
Extracted Fields
```

---

## Business Field Extraction

### Objective

Transform extracted text into validated business objects.

### Technologies

- Python
- Pydantic
- JSON
- OCR Output
- Structured Extraction

### Invoice Schema

Included fields:

- Invoice Number
- Customer
- Invoice Date
- Amount Due
- Services Provided
- Source Document
- Page Number

### Example Output

```json
{
  "invoice_number": "INV-1001",
  "customer": "ABC Trading Ltd",
  "invoice_date": "12 October 2026",
  "amount_due": "EUR 2500",
  "services_provided": "Consulting Services",
  "source_document": "INVOICE.pdf",
  "page_number": 1
}
```

### Validation

Missing fields are returned as:

```json
{
  "customer": null
}
```

instead of generating invalid values.

### Outcome

The Week 3 solution converts raw documents into validated, structured business objects suitable for APIs, databases, analytics, and downstream automation.

---

# Week 4 - FastAPI Service Layer

## Objective

Expose project functionality through REST APIs.

## Implemented Endpoints

### Home

```http
GET /
```

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

### RAG Query

```http
POST /rag/query
```

### Agent Query

```http
POST /agent/query
```

### Process Document

```http
POST /document/process
```

### Retrieve Stored Document

```http
GET /document/{document_id}
```

### Delete Stored Document

```http
DELETE /document/{document_id}
```

## Swagger Documentation

Available at:

```text
http://localhost:8000/docs
```

---

# Persistence and Security

## Persistence

Since Azure storage services were unavailable, local persistence was implemented.

### Storage Method

Processed documents are stored as JSON files inside:

```text
storage/
```

Example:

```json
{
  "id": "123",
  "file_name": "INVOICE.pdf",
  "status": "processed"
}
```

### Features

- Persistent storage across requests
- Retrieval by document ID
- Document deletion
- State maintained between API calls

## Security

### API Key Authentication

Secrets are stored in:

```text
.env
```

Example:

```text
API_KEY=rag123456
```

### Environment Variable Loading

Configuration is loaded using:

```python
python-dotenv
```

### Protected Endpoints

Retrieve and delete operations require:

```text
x-api-key
```

### Unauthorized Access

Returns:

```json
{
  "detail": "Unauthorized"
}
```

---

# Containerization

## Docker

### Build Image

```bash
docker build -t ai-assistant-api .
```

### Run Container

```bash
docker run -p 8000:8000 ai-assistant-api
```

### Verification

Health endpoint:

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

Azure deployment was not performed because an Azure environment was unavailable.

---

# Observability

## Features

### Structured Logging

Implemented application logging using Python logging.

### Request Correlation IDs

Each request receives:

```text
X-Request-ID
```

Example:

```text
ID=30be993e-0caa-4499-9f0a-b00e336ebcdf
```

### Request Tracing

```text
Request started | ID=...
Request completed | ID=... Status=200
```

### Error Visibility

Examples:

```text
401 Unauthorized
404 Not Found
500 Internal Server Error
```

---

# Automated Testing

## Test Coverage

Implemented automated tests for:

- Home Endpoint
- Health Endpoint
- RAG Endpoint
- Agent Endpoint
- Document Processing Endpoint

### Run Tests

```bash
pytest
```

### Result

```text
5 passed
```

---

# CI/CD Pipeline

## Technology

GitHub Actions

Pipeline file:

```text
.github/workflows/ci.yml
```

### Pipeline Workflow

```text
Code Push
    ↓
Install Dependencies
    ↓
Run Automated Tests
    ↓
Build Docker Image
    ↓
Create Deployable Artifact
```

### Automated Validation

The pipeline automatically:

- Installs dependencies
- Executes tests
- Builds Docker image
- Produces deployable artifacts

The workflow executes automatically on every push.

---

# Azure Alternatives Used

Azure resources were not available during development. Equivalent local implementations were used to demonstrate the same architectural concepts.

| Azure Service | Implemented Alternative |
|--------------|-------------------------|
| Azure Blob Storage | Local JSON Storage (`storage/`) |
| Azure Cosmos DB | JSON File Persistence |
| Azure Key Vault | `.env` + `python-dotenv` |
| Managed Identity | API Key Authentication |
| RBAC | API Key Authorization |
| Azure Application Insights | Structured Logging |
| Azure Monitor | Request Logs |
| Azure DevOps Pipelines | GitHub Actions |
| Azure Deployment | Docker Image + Deployable Artifact |

---

# Project Structure

```text
rag-ingestion/
│
├── app.py
├── test_app.py
├── Dockerfile
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── storage/
│
└── .github/
    └── workflows/
        └── ci.yml
```

---

# Outcome

The final solution provides:

✅ Retrieval-Augmented Generation (RAG)

✅ LangGraph agent orchestration

✅ Multi-tool routing

✅ MCP integration

✅ PDF intake and classification

✅ OCR processing

✅ Business field extraction and validation

✅ FastAPI backend services

✅ OpenAPI / Swagger documentation

✅ Persistent document storage

✅ Authentication and authorization

✅ Docker containerization

✅ Structured logging

✅ Request correlation IDs

✅ End-to-end request tracing

✅ Automated testing

✅ GitHub Actions CI/CD pipeline

✅ Deployable application artifact

The solution is fully functional locally and structured for future deployment to Azure or other cloud platforms.