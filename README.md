# Smart App - Intelligent Document Analysis Platform

A comprehensive document analysis application that supports multiple file types (PDF, Excel, Word, Audio, Video, JSON, etc.) with AI-powered insights using local and cloud-based language models.

## Features

- 🤖 Multi-model support (Ollama, HuggingFace, OpenAI)
- 📄 Process various file types: PDF, DOCX, XLSX, JSON, Audio, Video, Images
- 💬 ChatGPT-like interface for document interaction
- 🐳 Docker-based deployment for easy setup
- 🔍 Vector-based semantic search using PostgreSQL with pgvector
- 🎯 Modular and scalable architecture

## Architecture

- **Backend**: FastAPI (Python) - `smtapp_core`
- **Frontend**: React - `smtapp_client`
- **Database**: PostgreSQL with pgvector extension
- **LLM**: Ollama for local models
- **ORM**: SQLAlchemy

## Project Structure

```
Smart_app/
├── docker-compose.yml          # Docker orchestration
├── .env.example                # Environment variables template
├── config/                     # Global configuration files
│   └── app.toml               # Application settings
├── smtapp_core/               # FastAPI backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── config/                # Backend configuration
│   ├── models/                # SQLAlchemy models
│   ├── api/                   # API routes
│   ├── services/              # Business logic
│   ├── processors/            # File processors
│   └── utils/                 # Utilities
└── smtapp_client/             # React frontend
    ├── Dockerfile
    └── package.json
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AhsanZak/SmartApp.git
cd Smart_app
```

2. Copy the environment file:
```bash
cp .env.example .env
```

3. Start the application:
```bash
docker-compose up -d
```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Pull Ollama Models

After starting the services, pull the models you want to use:

```bash
docker exec -it smtapp_ollama ollama pull llama2
docker exec -it smtapp_ollama ollama pull mistral
```

## Development

### Backend Development

```bash
cd smtapp_core
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development

```bash
cd smtapp_client
npm install
npm start
```

## Configuration

Edit `config/app.toml` to configure:
- Database settings
- Model configurations
- API endpoints
- Processing options

## Supported File Types

- **Documents**: PDF, DOCX, TXT, MD
- **Spreadsheets**: XLSX, CSV
- **Data**: JSON, XML
- **Media**: MP3, MP4, WAV, AVI
- **Images**: JPG, PNG, GIF

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

