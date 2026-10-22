from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
from dotenv import load_dotenv

import json
import uuid
import os
import logging

from pathlib import Path

# ==========================================
# Environment Configuration
# ==========================================

env_path = Path(__file__).parent / ".env"

load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("API_KEY")

# ==========================================
# Logging Configuration
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="AI Assistant API",
    description="Week 4 FastAPI Backend",
    version="1.0"
)

# ==========================================
# Observability Middleware
# ==========================================

@app.middleware("http")
async def add_request_id(
    request: Request,
    call_next
):
    request_id = str(uuid.uuid4())

    logger.info(
        f"Request started | ID={request_id} "
        f"Method={request.method} "
        f"Path={request.url.path}"
    )

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    logger.info(
        f"Request completed | ID={request_id} "
        f"Status={response.status_code}"
    )

    return response


# ==========================================
# Request / Response Models
# ==========================================

class HealthResponse(BaseModel):
    status: str


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str


class DocumentRequest(BaseModel):
    file_name: str


class DocumentResponse(BaseModel):
    status: str
    file_name: str


class DocumentResult(BaseModel):
    id: str
    file_name: str
    status: str


# ==========================================
# Home Endpoint
# ==========================================

@app.get("/")
def home():
    return {
        "message": "AI Assistant API is running"
    }


# ==========================================
# Health Endpoint
# ==========================================

@app.get(
    "/health",
    response_model=HealthResponse
)
def health():

    return {
        "status": "healthy"
    }


# ==========================================
# RAG Query Endpoint
# ==========================================

@app.post(
    "/rag/query",
    response_model=QueryResponse
)
def rag_query(request: QueryRequest):

    try:

        if not request.question.strip():

            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )

        logger.info(
            f"RAG query received: {request.question}"
        )

        answer = f"RAG response for: {request.question}"

        return {
            "answer": answer
        }

    except HTTPException:
        raise

    except Exception:

        logger.error(
            "RAG service failed"
        )

        raise HTTPException(
            status_code=500,
            detail="RAG service failed"
        )


# ==========================================
# Agent Query Endpoint
# ==========================================

@app.post(
    "/agent/query",
    response_model=QueryResponse
)
def agent_query(request: QueryRequest):

    try:

        if not request.question.strip():

            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )

        logger.info(
            f"Agent query received: {request.question}"
        )

        answer = f"Agent response for: {request.question}"

        return {
            "answer": answer
        }

    except HTTPException:
        raise

    except Exception:

        logger.error(
            "Agent service failed"
        )

        raise HTTPException(
            status_code=500,
            detail="Agent service failed"
        )


# ==========================================
# Document Processing Endpoint
# ==========================================

@app.post(
    "/document/process",
    response_model=DocumentResult
)
def process_document(request: DocumentRequest):

    try:

        if not request.file_name.strip():

            raise HTTPException(
                status_code=400,
                detail="File name cannot be empty"
            )

        if not request.file_name.lower().endswith(".pdf"):

            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )

        logger.info(
            f"Processing document: {request.file_name}"
        )

        document_id = str(uuid.uuid4())

        result = {
            "id": document_id,
            "file_name": request.file_name,
            "status": "processed"
        }

        os.makedirs("storage", exist_ok=True)

        with open(
            f"storage/{document_id}.json",
            "w"
        ) as f:

            json.dump(result, f)

        logger.info(
            f"Document stored with ID: {document_id}"
        )

        return result

    except HTTPException:
        raise

    except Exception:

        logger.error(
            "Document processing failed"
        )

        raise HTTPException(
            status_code=500,
            detail="Document processing failed"
        )


# ==========================================
# Retrieve Document By ID
# ==========================================

@app.get(
    "/document/{document_id}",
    response_model=DocumentResult
)
def get_document(
    document_id: str,
    x_api_key: str = Header(...)
):

    if x_api_key != API_KEY:

        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    logger.info(
        f"Retrieving document: {document_id}"
    )

    path = f"storage/{document_id}.json"

    if not os.path.exists(path):

        logger.error(
            f"Document not found: {document_id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    with open(path, "r") as f:

        return json.load(f)


# ==========================================
# Delete Document By ID
# ==========================================

@app.delete("/document/{document_id}")
def delete_document(
    document_id: str,
    x_api_key: str = Header(...)
):

    if x_api_key != API_KEY:

        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    path = f"storage/{document_id}.json"

    if not os.path.exists(path):

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    os.remove(path)

    logger.info(
        f"Document deleted: {document_id}"
    )

    return {
        "message": "Document deleted",
        "id": document_id
    }