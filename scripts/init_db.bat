@echo off
REM Database Initialization Script for Windows
REM This script initializes the Smart App database

echo ================================================
echo Smart App - Database Initialization
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python first.
    exit /b 1
)

echo ✅ Python is installed
echo.

REM Check if we're using Docker or local setup
if exist "docker-compose.yml" (
    echo 🐳 Docker Compose detected
    echo.
    
    REM Check if containers are running
    docker-compose ps | findstr "smtapp_postgres.*Up" >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  PostgreSQL container is not running
        echo Starting PostgreSQL...
        docker-compose up -d postgres
        echo ⏳ Waiting for PostgreSQL to be ready...
        timeout /t 5 /nobreak >nul
    ) else (
        echo ✅ PostgreSQL container is running
    )
    
    echo.
    echo 🚀 Initializing database...
    
    REM Check if backend container is running
    docker-compose ps | findstr "smtapp_backend.*Up" >nul 2>&1
    if errorlevel 1 (
        REM Run locally
        echo Running locally...
        cd smtapp_core
        python init_db.py %*
    ) else (
        REM Run inside backend container
        echo Running inside backend container...
        docker-compose exec backend python init_db.py %*
    )
) else (
    echo 📂 Local setup detected
    echo.
    echo 🚀 Initializing database...
    cd smtapp_core
    python init_db.py %*
)

echo.
echo ================================================
echo Done!
echo ================================================

