# Razers AI

**A desktop AI assistant built with React, Electron, FastAPI, and OpenAI API.**

Razers AI is a desktop AI assistant project designed to provide an interactive AI chat experience through a modern interface. It uses React and Vite for the frontend, Electron for the desktop application architecture, and FastAPI for the backend.

> **Project Status:** In Development

## Features

- Modern chat interface
- Send and receive messages through the backend API
- Multiple conversations
- Conversation history stored locally using Local Storage
- Automatic conversation titles
- Backend health monitoring
- REST API integration between frontend and backend
- OpenAI API integration using the Responses API
- Loading indicator while waiting for AI responses
- Error handling for failed API requests
- Retry failed messages
- Responsive user interface

## Tech Stack

### Frontend
- React
- Vite
- Electron
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
│   └── vite.config.js
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

Make sure you have installed:

- Python
- Node.js and npm
- Git
- OpenAI API key

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
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the `backend` directory:

```env
OPENAI_API_KEY=your_openai_api_key
```

**Important:**
- Keep your API key private.
- Never commit the `.env` file to GitHub.
- Use `.env.example` as a template without including real credentials.

### 4. Start Backend Server

```bash
uvicorn main:app --reload
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

## Development Roadmap

### Completed

- [x] Backend Foundation
- [x] Frontend Foundation
- [x] Functional Chat Interface
- [x] Modern UI Design
- [x] Backend Health Check
- [x] Conversation History
- [x] Local Storage Persistence
- [x] OpenAI SDK Installation
- [x] OpenAI API Configuration
- [x] OpenAI Responses API Integration
- [x] Chat Loading Indicator
- [x] Frontend Error Handling
- [x] Retry Failed Messages
- [x] Chat Experience Polish

### In Progress

- [ ] End-to-End AI Response Testing
- [ ] Conversation Context and Memory

### Planned

- [ ] Database Integration
- [ ] Desktop Application Packaging
- [ ] Docker Production Setup
- [ ] Production Deployment

## Current Development Status

The OpenAI API integration has been implemented in the FastAPI backend using the OpenAI Responses API and the `gpt-4.1-mini` model.

The backend has successfully reached the OpenAI API and passed authentication. However, successful AI response testing is still pending because the API account currently has no remaining credits.

The frontend chat experience has been improved with a loading indicator, error handling, and a retry mechanism for failed messages.

Conversation history is currently stored in the browser using Local Storage. Database persistence and desktop application packaging are planned for future development.

## Security

- API credentials are stored in backend environment variables.
- The `.env` file is excluded from Git tracking.
- API requests are handled by the backend rather than exposing credentials in the frontend.

## Future Goals

Razers AI aims to evolve into a personal desktop assistant with:

- Persistent conversation memory
- Database-backed conversation management
- Improved AI interaction
- Native desktop experience
- Production-ready deployment

## Author

**RazersDev**

GitHub: [@razersdev](https://github.com/razersdev)

---

*Built with curiosity, consistency, and a passion for technology.*