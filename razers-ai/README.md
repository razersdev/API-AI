# Razers AI

**A desktop AI assistant built with React, Electron, FastAPI, and OpenAI API.**

Razers AI is a personal AI desktop assistant designed to provide an interactive AI chat experience through a modern interface. It uses React and Vite for the frontend, Electron for the desktop application architecture, and FastAPI for the backend.

> **Project Status:** In Development

---

## Features

### Chat Experience
- Modern and responsive chat interface
- Send and receive messages through the backend API
- AI response loading indicator
- Error handling for failed API requests
- Retry failed messages
- Conversation context handling

### Conversation Management
- Multiple conversations
- Create new conversations
- Automatic conversation titles
- Rename conversations
- Delete conversations
- Custom confirmation modal
- Custom toast notifications
- Conversation history stored locally using Local Storage
- Automatic local data persistence

### Backend Integration
- REST API integration between frontend and backend
- Backend health monitoring
- OpenAI API integration using the Responses API
- Environment-based configuration
- Mock Mode for development and testing
- HTTP error handling

---

## Tech Stack

### Frontend
- React
- Vite
- Electron (desktop architecture in development)
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic
- Python-dotenv
- OpenAI Python SDK

### AI Integration
- OpenAI API
- OpenAI Responses API
- GPT-4.1 mini (`gpt-4.1-mini`)

---

## Project Structure

```text
razers-ai/
├── frontend/
│   ├── electron/
│   │   └── main.cjs
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

Make sure you have installed:

- Python
- Node.js and npm
- Git
- OpenAI API key (required for real AI responses)

### 1. Clone Repository

```bash
git clone https://github.com/razersdev/API-AI.git
cd API-AI
```

### 2. Run Backend

Open a terminal:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the `backend` directory.

For development without API credits, use Mock Mode:

```env
MOCK_MODE=true
```

For real AI responses, configure your OpenAI API key:

```env
MOCK_MODE=false
OPENAI_API_KEY=your_openai_api_key
```

**Important:**
- Keep your API key private.
- Never commit the `.env` file to GitHub.
- Use `.env.example` as a template without including real credentials.
- Mock Mode allows frontend and backend development without making real OpenAI API requests.

### 4. Start Backend Server

From the `backend` directory:

```bash
python -m uvicorn main:app --reload
```

Backend runs at:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

Health check:

`http://127.0.0.1:8000/health`

### 5. Run Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

`http://localhost:5173`

---

## Development Roadmap

### Completed

- [x] Backend Foundation
- [x] Frontend Foundation
- [x] Functional Chat Interface
- [x] Modern UI Design
- [x] Backend Health Check
- [x] REST API Integration
- [x] OpenAI SDK Installation
- [x] OpenAI API Configuration
- [x] OpenAI Responses API Integration
- [x] Chat Loading Indicator
- [x] Frontend Error Handling
- [x] Retry Failed Messages
- [x] Conversation History
- [x] Local Storage Persistence
- [x] Multiple Conversations
- [x] Automatic Conversation Titles
- [x] Create New Conversation
- [x] Rename Conversation
- [x] Delete Conversation
- [x] Custom Confirmation Modal
- [x] Custom Toast Notifications
- [x] Conversation Management
- [x] Backend Configuration Audit
- [x] Frontend Configuration Audit
- [x] Environment & Dependency Audit
- [x] Backend API Testing
- [x] HTTP Exception Handling Improvement
- [x] Git Checkpoint and GitHub Push

### In Progress

- [ ] End-to-End Testing
  - [x] System Audit & Preparation
  - [x] Backend API Testing
  - [ ] Frontend Interaction Testing
  - [ ] Full-Stack Integration Testing
  - [ ] Error & Failure Scenario Testing
  - [ ] Regression Testing
  - [ ] Final E2E Validation
- [ ] End-to-End AI Response Testing
- [ ] Conversation Context and Memory Improvements

### Planned

- [ ] Database Integration
- [ ] Persistent Conversation Memory
- [ ] Electron Desktop Application Integration
- [ ] Desktop Application Packaging
- [ ] Docker Production Setup
- [ ] Production Deployment

---

## Current Development Status

Razers AI has completed its initial chat foundation and conversation management features.

The frontend supports multiple conversations, automatic conversation titles, local conversation persistence, rename and delete operations, custom confirmation modals, and toast notifications.

The FastAPI backend provides chat and health-check endpoints. OpenAI integration has been implemented using the Responses API with the `gpt-4.1-mini` model.

The backend is currently at version **0.6.1**.

Mock Mode is available for development and testing without requiring active OpenAI API credits.

### Testing Progress

The project is currently undergoing CP38 — End-to-End Testing.

- **CH01 — System Audit & Preparation:** Completed
- **CH02 — Backend API Testing:** Completed
- **Git Checkpoint:** Committed and pushed to GitHub
- **CH03 — Frontend Interaction Testing:** Next

The successful live OpenAI response still requires further verification. Previous testing encountered an API quota limitation.

### Current Architecture

- Frontend: React + Vite
- Backend: Python + FastAPI
- AI Provider: OpenAI Responses API
- Conversation Storage: Browser Local Storage
- Desktop Architecture: Electron integration in development
- Containerization: Docker configuration not yet implemented

Conversation history is currently stored in browser Local Storage and sent to the backend as conversation context. Database-backed persistence and more advanced memory capabilities remain part of the development roadmap.

---

## Security

- API credentials are stored in backend environment variables.
- The `.env` file is excluded from Git tracking.
- API requests are handled by the backend rather than exposing credentials in the frontend.
- Mock Mode can be used for development without real API credentials.

---

## Future Goals

Razers AI aims to evolve into a personal desktop assistant with:

- Persistent conversation memory
- Database-backed conversation management
- Improved AI interaction
- Native desktop experience
- Production-ready architecture
- Reliable and scalable backend services
- Docker-based deployment

---

## Author

**RazersDev**

GitHub: [@razersdev](https://github.com/razersdev)

Repository: [Razers AI](https://github.com/razersdev/API-AI)

---

*Built with curiosity, consistency, and a passion for technology.*