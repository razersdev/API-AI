
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI, OpenAIError
from pydantic import BaseModel, Field


# ==========================================
# ENVIRONMENT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MOCK_MODE = os.getenv(
    "MOCK_MODE",
    "true"
).lower() == "true"


# ==========================================
# OPENAI CLIENT
# ==========================================

client = None

if OPENAI_API_KEY:
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Razers AI API",
    description="Backend API for Razers AI Desktop",
    version="0.4.0"
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

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


# ==========================================
# REQUEST & RESPONSE SCHEMAS
# ==========================================

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]

    content: str = Field(
        min_length=1,
        max_length=10000
    )


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(
        min_length=1,
        max_length=50
    )


class ChatResponse(BaseModel):
    reply: str


# ==========================================
# MOCK RESPONSE GENERATOR
# ==========================================

def generate_mock_reply(
    messages: list[ChatMessage]
) -> str:

    latest_message = messages[-1].content

    previous_messages = messages[:-1]

    previous_user_messages = [
        message.content
        for message in previous_messages
        if message.role == "user"
    ]

    if previous_user_messages:

        previous_message = previous_user_messages[-1]

        return (
            "Halo! Aku Razers AI. 🤖\n\n"
            "Saat ini aku sedang berjalan dalam MOCK MODE.\n\n"
            f"Pesan sebelumnya: {previous_message}\n\n"
            f"Pesan terbaru: {latest_message}\n\n"
            f"Total pesan yang diterima: {len(messages)}\n\n"
            "Backend berhasil menerima riwayat percakapan kamu!"
        )

    return (
        "Halo! Aku Razers AI. 🤖\n\n"
        "Saat ini aku sedang berjalan dalam MOCK MODE.\n\n"
        f"Pesan kamu: {latest_message}\n\n"
        "Backend berhasil menerima pesan kamu!"
    )


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "app": "Razers AI",
        "status": "running",
        "version": "0.4.0",
        "mode": "mock" if MOCK_MODE else "production"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "mode": "mock" if MOCK_MODE else "production",
        "openai_configured": client is not None
    }


# ==========================================
# AI CHAT ENDPOINT
# ==========================================

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    # Ensure the latest message comes from the user

    if request.messages[-1].role != "user":

        raise HTTPException(
            status_code=422,
            detail="The last message must come from the user."
        )

    # MOCK MODE

    if MOCK_MODE:

        return ChatResponse(
            reply=generate_mock_reply(
                request.messages
            )
        )

    # Check OpenAI configuration

    if not client:

        raise HTTPException(
            status_code=503,
            detail="OpenAI API Key belum dikonfigurasi."
        )

    # Convert messages into OpenAI input format

    conversation_history = [
        {
            "role": item.role,
            "content": item.content
        }
        for item in request.messages
    ]

    # OPENAI REQUEST

    try:

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=conversation_history
        )

        reply = response.output_text

        if not reply:

            raise HTTPException(
                status_code=502,
                detail="OpenAI returned an empty response."
            )

        return ChatResponse(
            reply=reply
        )

    except HTTPException:

        raise

    except OpenAIError as error:

        print(
            f"OpenAI Error: {type(error).__name__}: {error}",
            flush=True
        )

        raise HTTPException(
            status_code=502,
            detail="OpenAI API request failed. Check backend terminal."
        ) from error

    except Exception as error:

        print(
            f"Unexpected Error: {type(error).__name__}: {error}",
            flush=True
        )

        raise HTTPException(
            status_code=500,
            detail="An unexpected backend error occurred."
        ) from error
