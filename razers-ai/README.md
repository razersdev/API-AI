# Razers AI

**Personal AI Assistant — Desktop Application**

Razers AI is a personal AI assistant project built with React, Vite, and FastAPI. The application is designed to provide an interactive AI chat experience with conversation history and contextual responses.

## Current Version

**Backend:** `0.7.0`  
**Project Status:** In Development

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

### Conversation Context Engine — v0.7.0
- Send previous messages as conversation context.
- Separate conversation history for each chat.
- System instructions for Razers AI identity and behavior.
- Dedicated conversation context builder.
- Configurable OpenAI model through environment variables.
- Message count and message length validation.

**Development status:** Implementation prepared; testing and verification pending.

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
cd API-AI
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
```

Configuration:

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key |
| `OPENAI_MODEL` | OpenAI model selection |
| `MOCK_MODE` | Enable or disable mock responses |

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

## Current Development Status

| Component | Status |
|---|---|
| React + Vite frontend | Implemented |
| FastAPI backend | Implemented |
| Local conversation storage | Implemented |
| OpenAI integration | Implemented |
| Mock Mode | Implemented |
| Conversation Context v0.7.0 | Testing pending |
| Electron integration | In development |
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