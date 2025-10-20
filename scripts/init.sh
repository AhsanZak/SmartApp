#!/bin/bash

# Smart App Initialization Script
# This script sets up the Smart App environment

echo "================================================"
echo "Smart App - Initialization Script"
echo "================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✅ Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker Compose is installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🚀 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo ""
echo "📊 Checking service status..."
docker-compose ps

echo ""
echo "================================================"
echo "✅ Smart App is now running!"
echo "================================================"
echo ""
echo "Access the application:"
echo "  🌐 Frontend:        http://localhost:3000"
echo "  🔧 Backend API:     http://localhost:8000"
echo "  📚 API Docs:        http://localhost:8000/docs"
echo "  🤖 Ollama:          http://localhost:11434"
echo ""
echo "Next steps:"
echo "  1. Pull Ollama models:"
echo "     docker exec -it smtapp_ollama ollama pull llama2"
echo ""
echo "  2. View logs:"
echo "     docker-compose logs -f"
echo ""
echo "  3. Stop services:"
echo "     docker-compose down"
echo ""
echo "For more information, see SETUP_GUIDE.md"
echo "================================================"

