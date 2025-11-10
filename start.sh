#!/bin/bash

# croXpost Quick Start Script
# This script helps you get started with the croXpost application

echo "🚀 croXpost Quick Start"
echo "======================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Setup environment files
echo "📝 Setting up environment files..."

if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env (please edit with your API keys)"
else
    echo "✅ backend/.env already exists"
fi

if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    echo "✅ Created frontend/.env"
else
    echo "✅ frontend/.env already exists"
fi

echo ""
echo "🐳 Starting Docker containers..."
echo "   This may take a few minutes on first run..."
echo ""

# Build and start containers
docker-compose up -d --build

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Initialize database
echo ""
echo "🗄️  Initializing database..."
docker-compose exec -T backend python init_db.py

echo ""
echo "✅ croXpost is ready!"
echo ""
echo "🌐 Access URLs:"
echo "   Frontend:    http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs:    http://localhost:8000/api/docs"
echo ""
echo "📖 Next steps:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Register a new account"
echo "   3. Start cross-posting!"
echo ""
echo "💡 Useful commands:"
echo "   Stop:     docker-compose down"
echo "   Restart:  docker-compose restart"
echo "   Logs:     docker-compose logs -f"
echo "   Cleanup:  docker-compose down -v"
echo ""
