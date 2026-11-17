# Razers AI

**Personal AI Assistant — Desktop Application**

Razers AI is a personal AI assistant project built with React, Vite, and FastAPI. The application is designed to provide an interactive AI chat experience with conversation history and contextual responses.

## Current Version

- **Backend:** `0.8.1`
- **Project Status:** In Development

## Features

### Implemented

- Interactive AI chat interface.
- Create new conversations.
- Conversation history management.
- Rename and delete conversations.
- Local conversation persistence using Local Storage.
- Backend health monitoring.
- Mock Mode for development and testing.
- OpenAI API integration.
- Retry failed messages.
- Copy AI responses.
- Backend request validation and error handling.

### Conversation Context Engine — v0.8.1

- Send previous messages as conversation context.
- Separate conversation history for each chat.
- Conversation identification using unique conversation IDs.
- System instructions for Razers AI identity and behavior.
- Dedicated conversation context builder.
- Token usage estimation for conversation messages.
- Conversation turn grouping to preserve complete exchanges.
- Context truncation based on a configurable token budget.
- Preserve the newest conversation turns when the context limit is reached.
- Configurable maximum context tokens through environment variables.
- Frontend conversation persistence across page refreshes.
- Conversation isolation between different chats.

**Development status:** Core implementation completed. Frontend persistence and conversation switching verified. Further context testing is the next step.

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS
- Browser Local Storage

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- Python-dotenv
- OpenAI Python SDK

### AI

- OpenAI Responses API
- Default model: `gpt-4.1-mini`

## Project Structure

```text
razers-ai/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env                  # Local only; never commit
│
├── frontend/
│   ├── electron/
│   │   └── main.cjs
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

Some components, including Electron and Docker configuration, are still under development.

## Getting Started

### 1. Clone Repository

```bash
git clone https://github.com/razersdev/API-AI.git
cd API-AI/razers-ai
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file inside the `backend` directory:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
MOCK_MODE=true
MAX_CONTEXT_TOKENS=12000
```

Configuration:

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key |
| `OPENAI_MODEL` | OpenAI model selection |
| `MOCK_MODE` | Enable or disable mock responses |
| `MAX_CONTEXT_TOKENS` | Maximum estimated context token budget |

**Important:** Never commit `.env` or expose your API key publicly.

### 4. Run Backend

From the `backend` directory:

```bash
python -m uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

### 5. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start development server:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Backend health check |
| POST | `/chat` | Send chat messages and conversation context |

### Chat Request Example

```json
{
  "conversation_id": "unique-conversation-id",
  "messages": [
    {
      "role": "user",
      "content": "My name is Razers."
    },
    {
      "role": "assistant",
      "content": "Hello, Razers!"
    },
    {
      "role": "user",
      "content": "What is my name?"
    }
  ]
}
```

The frontend sends the conversation ID and the relevant message history with each request.

The backend processes the supplied messages and applies context management before sending them to the AI model. Conversation history is currently managed by the frontend rather than persisted in a backend database.

## Conversation Context Management

The Conversation Context Engine introduces a context management layer to make conversation processing more efficient.

### Token Estimation

Estimates the token usage of messages before sending the conversation context to the AI model.

### Conversation Turn Grouping

Groups user messages and their corresponding assistant responses into complete conversation turns.

### Context Truncation

When the estimated context exceeds the configured token budget, older complete turns are removed while newer turns are preserved.

### Conversation Isolation

Each conversation has its own unique ID and message history. The frontend sends only the active conversation's history to the backend.

**Note:** Token estimation is approximate and is not an official tokenizer.

## Development Roadmap

### CP38 — End-to-End Testing

- CH01 — System Audit & Preparation
- CH02 — Backend API Testing
- CH03 — Frontend Interaction Testing
- CH04 — Full-Stack Integration Testing
- CH05 — Error & Failure Scenario Testing
- CH06 — Regression Testing
- CH07 — Final E2E Validation

### CP39 — Conversation Context Engine

- CH01 — Conversation Flow Audit
- CH02 — Context Management
- CH03 — Backend Integration
- CH04 — Frontend Integration
- CH05 — Context Testing

**Current focus:** CH05 — Context Testing.

## Current Development Status

| Component | Status |
|---|---|
| React + Vite frontend | Implemented |
| FastAPI backend | Implemented |
| Local conversation storage | Implemented |
| OpenAI integration | Implemented |
| Mock Mode | Implemented |
| Conversation Context Engine v0.8.1 | Implemented |
| Token estimation | Implemented |
| Conversation turn grouping | Implemented |
| Context truncation | Implemented |
| Conversation isolation | Verified |
| Frontend persistence | Verified |
| Electron integration | In Development |
| Docker configuration | Pending |

## Future Goals

- Streaming AI responses.
- Long-term AI memory.
- Edit and regenerate messages.
- File upload and document analysis.
- Voice assistant.
- Multiple AI providers.
- Local AI integration using Ollama.
- Desktop application packaging.
- Automated testing and deployment.

## Repository

GitHub: https://github.com/razersdev/API-AI

---

**Razers AI — Built to become a personal AI assistant.**
