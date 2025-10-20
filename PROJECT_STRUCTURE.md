# Smart App - Project Structure

Complete overview of the project architecture and structure.

## 📁 Project Layout

```
Smart_app/
├── docker-compose.yml              # Docker orchestration
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # Project overview
├── SETUP_GUIDE.md                  # Detailed setup instructions
├── PROJECT_STRUCTURE.md            # This file
│
├── config/                         # Global configuration
│   └── app.toml                    # Application settings (TOML)
│
├── scripts/                        # Utility scripts
│   ├── init.sh                     # Linux/Mac initialization
│   └── init.bat                    # Windows initialization
│
├── smtapp_core/                    # Backend (FastAPI)
│   ├── Dockerfile                  # Backend Docker config
│   ├── .dockerignore              # Docker ignore rules
│   ├── requirements.txt           # Python dependencies
│   ├── main.py                    # FastAPI application entry
│   ├── alembic.ini                # Database migration config
│   │
│   ├── config/                    # Backend configuration
│   │   ├── __init__.py
│   │   ├── settings.py            # Settings manager (Pydantic)
│   │   └── database.py            # Database connection & session
│   │
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── document.py            # Document & DocumentChunk models
│   │   ├── chat.py                # Chat & Message models
│   │   └── user.py                # User model
│   │
│   ├── api/                       # API endpoints (routes)
│   │   ├── __init__.py
│   │   ├── health.py              # Health check endpoints
│   │   ├── documents.py           # Document management API
│   │   ├── chat.py                # Chat API
│   │   └── models.py              # Model management API
│   │
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── document_service.py    # Document operations
│   │   ├── chat_service.py        # Chat operations
│   │   ├── model_service.py       # AI model operations
│   │   └── embedding_service.py   # Vector embeddings
│   │
│   ├── processors/                # File processors
│   │   ├── __init__.py
│   │   ├── base_processor.py      # Base processor class
│   │   ├── pdf_processor.py       # PDF processing
│   │   ├── docx_processor.py      # DOCX processing
│   │   ├── excel_processor.py     # Excel/CSV processing
│   │   ├── text_processor.py      # Text/JSON/XML processing
│   │   ├── audio_processor.py     # Audio processing
│   │   ├── video_processor.py     # Video processing
│   │   ├── image_processor.py     # Image processing
│   │   └── file_processor_factory.py  # Processor factory
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       └── helpers.py             # Helper functions
│
└── smtapp_client/                 # Frontend (React)
    ├── Dockerfile                 # Frontend Docker config
    ├── .dockerignore             # Docker ignore rules
    ├── package.json              # Node.js dependencies
    ├── README.md                 # Frontend documentation
    │
    ├── public/                   # Static files
    │   └── index.html           # HTML template
    │
    └── src/                     # React source code
        ├── index.js             # Entry point
        ├── index.css            # Global styles
        ├── App.js               # Main component
        └── App.css              # App styles
```

## 🏗️ Architecture Overview

### Backend Architecture (smtapp_core)

The backend follows a **layered architecture** with clear separation of concerns:

1. **API Layer** (`api/`)
   - RESTful endpoints
   - Request/response handling
   - Input validation
   - Route definitions

2. **Service Layer** (`services/`)
   - Business logic
   - Data orchestration
   - Complex operations
   - Cross-cutting concerns

3. **Data Layer** (`models/`)
   - SQLAlchemy ORM models
   - Database schema
   - Relationships
   - Data validation

4. **Processing Layer** (`processors/`)
   - File type-specific processors
   - Factory pattern implementation
   - Extensible processor system
   - Text extraction and analysis

5. **Configuration Layer** (`config/`)
   - Settings management
   - Database configuration
   - Environment variables
   - TOML configuration

### Frontend Architecture (smtapp_client)

The frontend is built with **React** and follows a component-based architecture:

- Currently: Basic setup with placeholder UI
- Planned: ChatGPT-like interface with Material-UI

## 🗄️ Database Schema

### Tables

1. **users**
   - User authentication and profiles
   - Fields: id, username, email, hashed_password, etc.

2. **documents**
   - Uploaded documents metadata
   - Fields: id, filename, file_type, extracted_text, embedding, etc.
   - Uses pgvector for semantic search

3. **document_chunks**
   - Document text chunks with embeddings
   - Fields: id, document_id, content, embedding, etc.

4. **chats**
   - Chat sessions
   - Fields: id, title, model_name, model_provider, etc.

5. **messages**
   - Chat messages (user & assistant)
   - Fields: id, chat_id, role, content, etc.

## 🔌 API Endpoints

### Health Endpoints
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/db` - Database health
- `GET /api/v1/health/detailed` - Detailed health status

### Document Endpoints
- `POST /api/v1/documents/upload` - Upload a document
- `GET /api/v1/documents` - List all documents
- `GET /api/v1/documents/{id}` - Get document by ID
- `DELETE /api/v1/documents/{id}` - Delete document

### Chat Endpoints
- `POST /api/v1/chats` - Create new chat
- `GET /api/v1/chats` - List all chats
- `GET /api/v1/chats/{id}` - Get chat with messages
- `POST /api/v1/chats/{id}/messages` - Send message
- `DELETE /api/v1/chats/{id}` - Delete chat

### Model Endpoints
- `GET /api/v1/models` - List available models
- `GET /api/v1/models/ollama` - List Ollama models
- `POST /api/v1/models/ollama/pull/{model}` - Pull Ollama model

## 🐳 Docker Services

1. **ollama** (ollama/ollama:latest)
   - Local LLM runtime
   - Port: 11434
   - Volume: ollama_data

2. **backend** (FastAPI)
   - Python 3.11
   - Port: 8000
   - Volumes: app code, uploads

3. **frontend** (React)
   - Node.js 18
   - Port: 3000
   - Volume: app code

## 🔧 Configuration Files

### 1. docker-compose.yml
- Service orchestration
- Network configuration
- Volume management
- Environment variables

### 2. config/app.toml
- Application settings
- Database configuration
- Ollama models
- Processing settings
- HuggingFace config

### 3. .env
- Environment-specific variables
- Secrets and credentials
- Service URLs

### 4. requirements.txt (Backend)
- Python dependencies
- FastAPI, SQLAlchemy, etc.
- ML/NLP libraries

### 5. package.json (Frontend)
- Node.js dependencies
- React, Material-UI, etc.

## 📊 Data Flow

### Document Upload Flow
```
User → Frontend → POST /documents/upload
     → Backend API
     → Save file to disk
     → Create DB record
     → Process file (extract text)
     → Create embeddings
     → Store in DB (with vector)
     → Return response
```

### Chat Flow
```
User → Enter message → Frontend
     → POST /chats/{id}/messages
     → Backend API
     → Retrieve chat history
     → Get document context (if any)
     → Call Ollama/Model
     → Store messages
     → Return AI response
     → Frontend displays
```

## 🧩 Design Patterns

1. **Factory Pattern**
   - `FileProcessorFactory` for creating processors
   - Extensible for new file types

2. **Repository Pattern**
   - Service layer abstracts data access
   - Clean separation from API layer

3. **Dependency Injection**
   - FastAPI's `Depends()`
   - Database session management

4. **Strategy Pattern**
   - Different processors for different file types
   - Model providers (Ollama, HuggingFace, etc.)

## 🔐 Security Considerations

1. **File Upload**
   - File type validation
   - Size limits
   - Filename sanitization
   - Secure storage

2. **Database**
   - SQLAlchemy ORM (prevents SQL injection)
   - Prepared statements
   - Connection pooling

3. **API**
   - CORS configuration
   - Request validation (Pydantic)
   - Error handling

4. **Authentication** (To be implemented)
   - JWT tokens
   - Password hashing
   - User sessions

## 📈 Scalability

### Current Setup
- Single-instance deployment
- Suitable for development and small-scale use

### Future Considerations
1. **Horizontal Scaling**
   - Multiple backend instances
   - Load balancer
   - Shared storage (S3, etc.)

2. **Caching**
   - Redis for sessions
   - Response caching
   - Model output caching

3. **Background Jobs**
   - Celery for async processing
   - Document processing queue
   - Batch embedding generation

4. **Database Optimization**
   - Read replicas
   - Connection pooling
   - Index optimization

## 🧪 Testing Strategy

To be implemented:
1. **Unit Tests**
   - Service layer
   - Processors
   - Utilities

2. **Integration Tests**
   - API endpoints
   - Database operations

3. **End-to-End Tests**
   - User workflows
   - Frontend + Backend

## 📚 Key Technologies

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database
- **PostgreSQL + pgvector**: Vector database
- **Ollama**: Local LLM runtime
- **Sentence Transformers**: Text embeddings
- **pypdf, python-docx, openpyxl**: File processing

### Frontend
- **React 18**: UI library
- **Material-UI**: Component library
- **Axios**: HTTP client
- **React Query**: Data fetching

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## 🚀 Future Enhancements

1. **Authentication System**
2. **Real-time Chat with WebSockets**
3. **Advanced File Processing (OCR, Transcription)**
4. **Multiple Model Providers**
5. **Collaborative Features**
6. **Analytics Dashboard**
7. **Mobile App**

---

For setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)
For project overview, see [README.md](README.md)

