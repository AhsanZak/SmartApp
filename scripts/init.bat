@echo off
REM Smart App Initialization Script for Windows
REM This script sets up the Smart App environment

echo ================================================
echo Smart App - Initialization Script
echo ================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    exit /b 1
)

echo ✅ Docker is installed

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

echo ✅ Docker Compose is installed
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from .env.example...
    copy .env.example .env
    echo ✅ .env file created
) else (
    echo ✅ .env file already exists
)

echo.
echo 🚀 Starting Docker containers...
docker-compose up -d

echo.
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check if services are running
echo.
echo 📊 Checking service status...
docker-compose ps

echo.
echo ================================================
echo ✅ Smart App is now running!
echo ================================================
echo.
echo Access the application:
echo   🌐 Frontend:        http://localhost:3000
echo   🔧 Backend API:     http://localhost:8000
echo   📚 API Docs:        http://localhost:8000/docs
echo   🤖 Ollama:          http://localhost:11434
echo.
echo Next steps:
echo   1. Pull Ollama models:
echo      docker exec -it smtapp_ollama ollama pull llama2
echo.
echo   2. View logs:
echo      docker-compose logs -f
echo.
echo   3. Stop services:
echo      docker-compose down
echo.
echo For more information, see SETUP_GUIDE.md
echo ================================================

