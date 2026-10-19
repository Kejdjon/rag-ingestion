from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="AI Assistant API",
    description="Week 4 FastAPI Backend",
    version="1.0"
)


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

        # Replace with your rag.py call
        answer = (
            f"RAG response for: "
            f"{request.question}"
        )

        return {
            "answer": answer
        }

    except HTTPException:
        raise

    except Exception:

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

        # Replace with your graph.py call
        answer = (
            f"Agent response for: "
            f"{request.question}"
        )

        return {
            "answer": answer
        }

    except HTTPException:
        raise

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Agent service failed"
        )


# ==========================================
# Document Processing Endpoint
# ==========================================

@app.post(
    "/document/process",
    response_model=DocumentResponse
)
def process_document(request: DocumentRequest):

    try:

        if not request.file_name.strip():

            raise HTTPException(
                status_code=400,
                detail="File name cannot be empty"
            )

        # Replace with your intake/ocr/extraction logic

        return {
            "status": "processed",
            "file_name": request.file_name
        }

    except HTTPException:
        raise

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Document processing failed"
        )