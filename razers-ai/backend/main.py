
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import (
    OpenAI,
    OpenAIError,
    APIConnectionError,
    APITimeoutError,
    APIStatusError
)
from pydantic import BaseModel, Field


# ==========================================
# ENVIRONMENT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MOCK_MODE = os.getenv(
    "MOCK_MODE",
    "true"
).strip().lower() == "true"


# ==========================================
# CONFIGURATION DEBUGGING
# ==========================================

print("\n========== RAZERS AI CONFIG ==========")
print("ENV PATH:", ENV_PATH)
print("ENV FILE EXISTS:", ENV_PATH.exists())
print("MOCK MODE:", MOCK_MODE)
print("OPENAI API KEY LOADED:", bool(OPENAI_API_KEY))
print("======================================\n")


# ==========================================
# OPENAI CLIENT
# ==========================================

client = None

if OPENAI_API_KEY:
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        timeout=30.0,
        max_retries=2
    )


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Razers AI API",
    description="Backend API for Razers AI Desktop",
    version="0.6.0"
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
        "version": "0.6.0",
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

    # Validate latest message

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

    # Convert conversation history

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
                detail="AI tidak memberikan respons. Silakan coba lagi."
            )

        return ChatResponse(
            reply=reply
        )

    # TIMEOUT ERROR

    except APITimeoutError as error:

        print(
            f"OpenAI Timeout: {error}",
            flush=True
        )

        raise HTTPException(
            status_code=504,
            detail="Waktu tunggu AI habis. Silakan coba lagi."
        ) from error

    # CONNECTION ERROR

    except APIConnectionError as error:

        print(
            f"OpenAI Connection Error: {error}",
            flush=True
        )

        raise HTTPException(
            status_code=503,
            detail="Gagal terhubung ke OpenAI. Periksa koneksi internet kamu."
        ) from error

    # OPENAI API STATUS ERRORS

    except APIStatusError as error:

        status_code = error.status_code

        print(
            f"OpenAI API Error: {status_code} - {type(error).__name__}",
            flush=True
        )

        if status_code == 400:

            detail = "Permintaan tidak valid. Periksa pesan yang dikirim."

        elif status_code == 401:

            detail = "OpenAI API Key tidak valid. Periksa konfigurasi API Key."

        elif status_code == 403:

            detail = "Akses OpenAI API ditolak. Periksa izin akun kamu."

        elif status_code == 404:

            detail = "Model AI tidak ditemukan atau tidak tersedia."

        elif status_code == 429:

            detail = (
                "Kuota API habis atau batas penggunaan tercapai. "
                "Periksa billing dan usage OpenAI."
            )

        elif status_code >= 500:

            detail = "Layanan OpenAI sedang mengalami gangguan. Coba lagi nanti."

        else:

            detail = "OpenAI API mengalami kesalahan. Silakan coba lagi."

        raise HTTPException(
            status_code=status_code if status_code in [
                400, 401, 403, 404, 429
            ] else 502,
            detail=detail
        ) from error

    # OTHER OPENAI ERRORS

    except OpenAIError as error:

        print(
            f"OpenAI Error: {type(error).__name__}: {error}",
            flush=True
        )

        raise HTTPException(
            status_code=502,
            detail="Terjadi kesalahan pada layanan AI."
        ) from error

    # UNEXPECTED BACKEND ERRORS

    except Exception as error:

        print(
            f"Unexpected Error: {type(error).__name__}: {error}",
            flush=True
        )

        raise HTTPException(
            status_code=500,
            detail="Terjadi kesalahan pada backend Razers AI."
        ) from error
