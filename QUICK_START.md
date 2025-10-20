# Quick Start Guide

Get Smart App running in 5 minutes!

## 🚀 One-Command Setup

### Windows
```bash
scripts\init.bat
```

### Linux/Mac
```bash
chmod +x scripts/init.sh
./scripts/init.sh
```

## 🎯 Manual Setup (3 Steps)

### Step 1: Start Services
```bash
docker-compose up -d
```

### Step 2: Initialize Database
```bash
# Windows
scripts\init_db.bat

# Linux/Mac
./scripts/init_db.sh
```

### Step 3: Ensure remote Ollama has a model
```bash
ssh user@192.168.100.25 "ollama pull llama2"
```

### Step 4: Access Application
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## ✅ Verify Installation

### Check Health
```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-...",
  "service": "Smart App API"
}
```

### Check Available Models
```bash
curl http://localhost:8000/api/v1/models/ollama
```

## 📤 Upload Your First Document

### Using cURL
```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@document.pdf"
```

### Using API Docs
1. Go to http://localhost:8000/docs
2. Find `POST /api/v1/documents/upload`
3. Click "Try it out"
4. Upload file
5. Execute

## 💬 Create Your First Chat

### Using cURL
```bash
# 1. Create chat
curl -X POST "http://localhost:8000/api/v1/chats" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Chat", "model_name": "llama2"}'

# Response: {"id": 1, ...}

# 2. Send message
curl -X POST "http://localhost:8000/api/v1/chats/1/messages" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello! How are you?"}'
```

### Using API Docs
1. Go to http://localhost:8000/docs
2. Create chat via `POST /api/v1/chats`
3. Send message via `POST /api/v1/chats/{chat_id}/messages`

## 🔧 Common Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild After Changes
```bash
docker-compose up -d --build
```

## 🐛 Troubleshooting

### Backend not starting?
```bash
docker logs smtapp_backend
```

### Ollama not responding?
```bash
# Check if models are pulled
docker exec -it smtapp_ollama ollama list

# Pull a model
docker exec -it smtapp_ollama ollama pull llama2
```

### Database connection error?
Using SQLite by default, so no database service is required. If you switched to PostgreSQL, refer to DATABASE_SETUP.md.

### Port already in use?
Edit `docker-compose.yml` and change port mappings:
```yaml
ports:
  - "8001:8000"  # Change 8000 to 8001
```

## 📊 Available Models

Popular Ollama models to try:

```bash
# Small and fast (recommended for testing)
docker exec -it smtapp_ollama ollama pull llama2

# More capable
docker exec -it smtapp_ollama ollama pull mistral

# Code-focused
docker exec -it smtapp_ollama ollama pull codellama

# Larger and more powerful
docker exec -it smtapp_ollama ollama pull llama3
```

## 📁 Supported File Types

- **Documents**: PDF, DOCX, TXT, MD
- **Spreadsheets**: XLSX, CSV
- **Data**: JSON, XML
- **Media**: MP3, MP4, WAV, AVI (metadata only for now)
- **Images**: JPG, PNG, GIF (metadata only for now)

## 🎓 Next Steps

1. **Explore API**: Visit http://localhost:8000/docs
2. **Read Documentation**: Check out `README.md` and `SETUP_GUIDE.md`
3. **Customize**: Edit `config/app.toml` for your needs
4. **Develop Frontend**: See `smtapp_client/README.md`

## 💡 Pro Tips

1. **API Testing**: Use the built-in Swagger UI at `/docs`
2. **Model Selection**: Different models have different strengths
3. **File Size**: Default max is 100MB (configurable)
4. **Context**: Include document IDs when chatting for document-aware responses

## 🆘 Need Help?

- **Full Documentation**: See `SETUP_GUIDE.md`
- **Project Structure**: See `PROJECT_STRUCTURE.md`
- **Issues**: GitHub Issues

---

**You're all set! Happy coding! 🎉**

