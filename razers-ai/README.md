# Razers AI

**Personal AI Assistant — Desktop Application**

Razers AI is a personal AI assistant project built with React, Vite, and FastAPI. The application is designed to provide an interactive AI chat experience with conversation history, contextual responses, and persistent user memory.

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
- Conversation Context Engine.
- Persistent Memory system using SQLite.
- Keyword-based memory retrieval.
- Category-based memory filtering.
- Importance-based memory prioritization.
- Cross-conversation memory retrieval.
- Memory retrieval failure handling.
- Memory CRUD repository and service.
- Memory Management API:
  - Retrieve memories.
  - Retrieve a memory by ID.
  - Create a memory.
  - Update an existing memory.

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

**Development status:** Core implementation completed. Frontend persistence, conversation switching, and context management have been verified.

### Persistent Memory — CP40

- SQLite-based persistent memory storage.
- SQLAlchemy ORM integration.
- Alembic database migration support.
- Dedicated memory data model.
- Memory repository for database queries.
- Memory retrieval service.
- Keyword-based memory search.
- Category-based memory filtering.
- Memory prioritization using importance values.
- Updated-time prioritization.
- Configurable memory retrieval limit.
- Persistent memory context builder.
- Integration with the `/chat` endpoint.
- Memory context integration with Mock Mode.
- Cross-conversation memory retrieval.
- Memory retrieval failure handling and graceful fallback.

**Development status:** Core persistent memory implementation completed. Memory storage, retrieval, filtering, prioritization, cross-conversation retrieval, failure handling, and chat integration have been validated.

**Testing:** 6/6 memory testing scenarios passed.

Live OpenAI production behavior with persistent memory remains pending further validation.

### Memory Management — CP41

The Memory Management module introduces API-level operations for managing stored memories.

**Implemented capabilities:**

- Retrieve all memories.
- Retrieve a memory by its unique ID.
- Create new memories.
- Update existing memories.
- Memory CRUD repository integration.
- Memory service integration.
- Pydantic request and response schemas.
- Database session handling.
- HTTP response handling, including `404 Not Found` for missing memory records.

**Development status:** CH01 — Memory Management Audit and CH02 — Memory CRUD Logic completed. CH03 — Memory Management API is currently in progress.

The API currently supports memory retrieval, creation, and updating. Memory deletion and additional validation and security improvements remain part of the development roadmap.

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
- SQLAlchemy
- Alembic

### Database

- SQLite
- SQLAlchemy ORM
- Alembic Migrations

### AI

- OpenAI Responses API
- Default model: `gpt-4.1-mini`

## Project Structure

```text
razers-ai/
│
├── backend/
│   ├── database/
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── memory_service.py
│   │
│   ├── migrations/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── main.py
│   ├── requirements.txt
│   └── alembic.ini
│
├── frontend/
│   ├── electron/
│   │   └── main.cjs
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   │
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

The local SQLite database is generated locally and should not be committed to the repository.

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

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file inside the `backend` directory.

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

### 4. Database Migration

Razers AI uses Alembic to manage database schema migrations.

From the backend directory, run:

```bash
python -m alembic upgrade head
```

This applies the available migrations and creates the required database tables.

### 5. Run Backend

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

### 6. Frontend Setup

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

### General Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Backend health check |
| POST | `/chat` | Send chat messages and conversation context |

### Memory Management Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/memories` | Retrieve stored memories |
| GET | `/memories/{memory_id}` | Retrieve a memory by ID |
| POST | `/memories` | Create a new memory |
| PUT | `/memories/{memory_id}` | Update an existing memory |

**Note:** Memory deletion endpoint is not implemented yet.

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

The frontend sends the conversation ID and relevant message history with each request.

The backend processes the supplied messages and applies context management before sending them to the AI model.

Conversation history is currently managed by the frontend rather than persisted in a backend database.

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

## Persistent Memory System

The Persistent Memory system introduces long-term memory capabilities to Razers AI.

Unlike conversation context, which only represents the active conversation history, persistent memory is designed to store selected information that can be retrieved across different conversations.

### Memory Architecture

The current memory architecture consists of:

- **SQLite:** Local persistent database.
- **SQLAlchemy:** Object-relational mapping.
- **Alembic:** Database schema migration management.
- **Memory Repository:** Handles database queries.
- **Memory Service:** Handles memory retrieval and management logic.
- **Memory Context Builder:** Formats retrieved memories into AI context.
- **Chat Integration:** Supplies relevant memory context to the chat pipeline.

### Memory Data Model

The initial memory model includes:

| Field | Description |
|---|---|
| `id` | Unique memory identifier |
| `content` | Stored memory content |
| `category` | Memory category |
| `source_conversation_id` | Source conversation identifier |
| `importance` | Memory importance value |
| `created_at` | Memory creation timestamp |
| `updated_at` | Last update timestamp |

### Memory Categories

The initial memory categories are:

- `personal`
- `preference`
- `project`
- `knowledge`

### Memory Retrieval

The retrieval engine currently supports:

- Keyword-based memory search.
- Category-based filtering.
- Importance-based prioritization.
- Updated-time prioritization.
- Configurable retrieval limits.

### Cross-Conversation Memory

Persistent memory retrieval is independent of the active conversation ID.

This allows relevant stored memory to be retrieved when a user starts a different conversation.

### Memory Integration with Chat

The chat pipeline retrieves relevant memories based on the latest user message.

Retrieved memory is formatted and supplied as additional context to the AI model.

The memory context is treated as reference data, not as system instructions.

### Memory Failure Handling

The memory retrieval system includes error handling to prevent memory retrieval failures from interrupting the chat application.

When memory retrieval fails, the system falls back to an empty memory context, allowing the application to continue processing without retrieved memories.

### Persistent Memory Testing

Persistent Memory has been validated through six testing scenarios:

| Test Scenario | Result |
|---|---|
| Memory Persistence | PASS |
| Memory Retrieval | PASS |
| Category Filtering | PASS |
| Importance Prioritization | PASS |
| Cross-Conversation Retrieval | PASS |
| Failure Handling | PASS |

**Testing result: 6/6 scenarios passed.**

Storage persistence, retrieval, filtering, prioritization, cross-conversation access, and failure handling have been validated.

Live production OpenAI API behavior with persistent memory remains pending validation.

## Memory Management API

The Memory Management API provides backend endpoints to manage persistent memory records.

### Available Operations

**Retrieve Memories**

```http
GET /memories
```

Retrieves stored memories.

**Retrieve Memory by ID**

```http
GET /memories/{memory_id}
```

Retrieves a specific memory using its unique ID.

**Create Memory**

```http
POST /memories
```

Example request:

```json
{
  "content": "Learning Memory Management API",
  "category": "knowledge",
  "importance": 4,
  "source_conversation_id": "conversation_001"
}
```

**Update Memory**

```http
PUT /memories/{memory_id}
```

Example request:

```json
{
  "content": "Completed Memory Management API implementation",
  "category": "project",
  "importance": 5
}
```

### Memory API Schemas

- **MemoryCreate:** Defines the data required to create a memory.
- **MemoryUpdate:** Defines optional fields for updating an existing memory.
- **MemoryResponse:** Defines the memory data returned by the API.

### API Development Status

- Memory retrieval endpoints: Tested.
- Memory creation endpoint: Tested.
- Memory update endpoint: Tested.
- Memory deletion endpoint: Pending.
- Additional validation and security: Pending.

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

**Status:** Core implementation completed.

### CP40 — Persistent Memory

- CH01 — Memory Architecture
- CH02 — Memory Data Model
- CH03 — Memory Storage Backend
- CH04 — Memory Retrieval Engine
- CH05 — Memory Integration with Chat
- CH06 — Memory Testing

**Status:** COMPLETED

**Final progress:**

- CH01 — CLEAR
- CH02 — CLEAR
- CH03 — CLEAR
- CH04 — CLEAR
- CH05 — CLEAR
- CH06 — CLEAR

**Final testing result: 6/6 PASS**

### CP41 — Memory Management

- CH01 — Memory Management Audit
- CH02 — Memory CRUD Logic
- CH03 — Memory Management API
- CH04 — Memory Validation & Security
- CH05 — Memory Management Testing

**Current progress:**

- CH01 — CLEAR
- CH02 — CLEAR
- CH03 — ACTIVE
- CH04 — LOCKED
- CH05 — LOCKED

**Current focus:** Completing the Memory Management API before moving to validation, security, and testing.

## Current Development Status

| Component | Status |
|---|---|
| React + Vite frontend | Implemented |
| FastAPI backend | Implemented |
| Local conversation storage | Implemented |
| OpenAI integration | Implemented |
| Mock Mode | Implemented |
| Conversation Context Engine v0.8.1 | Completed |
| Token estimation | Verified |
| Conversation turn grouping | Verified |
| Context truncation | Verified |
| Conversation isolation | Verified |
| Frontend persistence | Verified |
| SQLite memory storage | Implemented |
| SQLAlchemy ORM | Implemented |
| Alembic migrations | Verified |
| Memory repository | Implemented |
| Memory retrieval service | Implemented |
| Memory context builder | Implemented |
| Chat endpoint memory integration | Verified |
| Memory category filtering | Verified |
| Importance prioritization | Verified |
| Cross-conversation retrieval | Verified |
| Memory failure handling | Verified |
| Persistent Memory CP40 | Completed — 6/6 tests passed |
| Memory retrieval API | Verified |
| Memory creation API | Verified |
| Memory update API | Verified |
| Memory deletion API | Pending |
| Memory validation & security | Pending |
| Memory Management testing | Pending |
| Live production OpenAI memory validation | Pending |
| Electron integration | In Development |
| Docker configuration | Pending |

## Future Goals

- Complete Memory Management API, including deletion.
- Memory validation and security improvements.
- Comprehensive Memory Management testing.
- Streaming AI responses.
- Edit and regenerate messages.
- File upload and document analysis.
- Voice assistant.
- Multiple AI providers.
- Local AI integration using Ollama.
- Desktop application packaging.
- Automated testing and deployment.

## Repository

GitHub: https://github.com/razersdev/API