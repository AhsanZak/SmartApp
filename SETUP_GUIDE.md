# Smart App - Setup Guide

Complete setup guide for the Smart App - Intelligent Document Analysis Platform.

## Prerequisites

- Docker and Docker Compose (recommended)
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)
- Git

## Quick Start with Docker (Recommended)

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/AhsanZak/SmartApp.git
cd Smart_app

# Create environment file
cp .env.example .env

# Edit .env file if needed (optional)
```

### 2. Start All Services

```bash
# Build and start all containers
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3. Pull Ollama Models

After the services are running, pull the AI models you want to use:

```bash
# Pull Llama 2
docker exec -it smtapp_ollama ollama pull llama2

# Pull Mistral (optional)
docker exec -it smtapp_ollama ollama pull mistral

# Pull other models
docker exec -it smtapp_ollama ollama pull codellama
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Ollama**: http://localhost:11434
- **PostgreSQL**: localhost:5432

## Local Development Setup

### Backend Development

```bash
cd smtapp_core

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
set DATABASE_URL=postgresql://smtapp:smtapp123@localhost:5432/smtapp_db
set OLLAMA_BASE_URL=http://localhost:11434

# Run the application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd smtapp_client

# Install dependencies
npm install

# Start development server
npm start
```

## Configuration

### 1. Database Configuration

Edit `config/app.toml` to configure database settings:

```toml
[database]
dialect = "postgresql"
host = "postgres"
port = 5432
username = "smtapp"
password = "smtapp123"
database = "smtapp_db"
```

### 2. Ollama Configuration

```toml
[ollama]
base_url = "http://ollama:11434"
timeout = 120
default_model = "llama2"
```

### 3. File Processing Configuration

```toml
[processing]
max_file_size_mb = 100
supported_formats = [
    "pdf", "docx", "xlsx", "json",
    "mp3", "mp4", "jpg", "png"
]
```

## Testing the API

### 1. Health Check

```bash
curl http://localhost:8000/api/v1/health
```

### 2. List Available Models

```bash
curl http://localhost:8000/api/v1/models
```

### 3. Upload a Document

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf"
```

### 4. Create a Chat

```bash
curl -X POST "http://localhost:8000/api/v1/chats" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Chat", "model_name": "llama2"}'
```

## Database Migrations

### Create a Migration

```bash
cd smtapp_core
alembic revision --autogenerate -m "description"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migrations

```bash
alembic downgrade -1
```

## Troubleshooting

### Issue: Ollama service not responding

```bash
# Check Ollama logs
docker logs smtapp_ollama

# Restart Ollama
docker restart smtapp_ollama
```

### Issue: Database connection errors

```bash
# Check PostgreSQL logs
docker logs smtapp_postgres

# Recreate database
docker-compose down -v
docker-compose up -d postgres
```

### Issue: Frontend not connecting to backend

Check that:
1. Backend is running on port 8000
2. CORS is configured correctly
3. `REACT_APP_API_URL` is set correctly in frontend

## Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Rebuild services
docker-compose up -d --build

# View logs
docker-compose logs -f [service_name]

# Execute command in container
docker exec -it smtapp_backend bash

# Remove volumes (WARNING: deletes data)
docker-compose down -v
```

## Monitoring

### Check Service Status

```bash
docker-compose ps
```

### View Resource Usage

```bash
docker stats
```

### Check API Health

```bash
curl http://localhost:8000/api/v1/health/detailed
```

## Production Deployment

For production deployment:

1. Change all default passwords in `.env`
2. Set `debug = false` in `config/app.toml`
3. Configure proper CORS origins
4. Set up SSL/TLS certificates
5. Use production-grade database
6. Set up proper logging and monitoring
7. Configure backup strategy

## Support

For issues and questions:
- GitHub Issues: https://github.com/AhsanZak/SmartApp/issues
- Documentation: See README.md

## Next Steps

1. **Backend**: The FastAPI backend is fully set up with OOP architecture
2. **Frontend**: Basic React structure is ready - UI components need to be implemented
3. **Models**: Pull the Ollama models you need
4. **Testing**: Test the API endpoints using the Swagger docs at http://localhost:8000/docs

Enjoy using Smart App! 🚀

