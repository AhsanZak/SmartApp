#!/bin/bash

# Database Initialization Script for Linux/Mac
# This script initializes the Smart App database

echo "================================================"
echo "Smart App - Database Initialization"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 is installed"
echo ""

# Check if we're using Docker or local setup
if [ -f "docker-compose.yml" ]; then
    echo "🐳 Docker Compose detected"
    echo ""
    
    # Check if containers are running
    if docker-compose ps | grep -q "smtapp_postgres.*Up"; then
        echo "✅ PostgreSQL container is running"
    else
        echo "⚠️  PostgreSQL container is not running"
        echo "Starting PostgreSQL..."
        docker-compose up -d postgres
        echo "⏳ Waiting for PostgreSQL to be ready..."
        sleep 5
    fi
    
    echo ""
    echo "🚀 Initializing database..."
    
    # Run init script inside backend container if it's running
    if docker-compose ps | grep -q "smtapp_backend.*Up"; then
        echo "Running inside backend container..."
        docker-compose exec backend python init_db.py "$@"
    else
        # Run locally
        echo "Running locally..."
        cd smtapp_core
        python3 init_db.py "$@"
    fi
else
    echo "📂 Local setup detected"
    echo ""
    echo "🚀 Initializing database..."
    cd smtapp_core
    python3 init_db.py "$@"
fi

echo ""
echo "================================================"
echo "Done!"
echo "================================================"

