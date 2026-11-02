# Razers AI

**A desktop AI assistant built with React, Electron, and FastAPI.**

Razers AI is a desktop assistant project designed to provide an interactive chat experience through a modern desktop interface. It uses React and Electron for the frontend and FastAPI for the backend.

> **Project Status:** In Development 

## Features

- Modern desktop-inspired chat interface
- Send and receive messages
- Multiple conversations
- Conversation history stored locally using Local Storage
- Automatic conversation titles
- Backend health monitoring
- REST API integration between frontend and backend
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
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Backend runs at:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

### 3. Run Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

`http://localhost:5173`

## Development Roadmap

- [x] Backend Foundation
- [x] Frontend Foundation
- [x] Functional Chat Interface
- [x] Modern UI Design
- [x] Backend Health Check
- [x] Conversation History
- [x] Local Storage Persistence
- [ ] AI Model Integration
- [ ] Database Integration
- [ ] Desktop Application Packaging
- [ ] Production Deployment

## Current Limitations

- Chat responses currently use a placeholder backend response.
- Conversation history is stored locally in the browser.
- AI model integration is not yet implemented.

## Author

**RazersDev**

GitHub: [@razersdev](https://github.com/razersdev)

---


