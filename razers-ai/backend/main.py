
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Razers AI API",
    description="Backend API for Razers AI Desktop",
    version="0.1.0"
)

# Frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Chat request schema
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)


# Chat response schema
class ChatResponse(BaseModel):
    reply: str


# Root endpoint
@app.get("/")
def home():
    return {
        "app": "Razers AI",
        "status": "running"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return ChatResponse(
        reply=f"Pesan kamu berhasil diterima: {request.message}"
    )
