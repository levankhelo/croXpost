#!/bin/bash

# Health check script for croXpost
# Verifies all services are running correctly

echo "🏥 croXpost Health Check"
echo "========================"
echo ""

# Function to check if a port is open
check_port() {
    local port=$1
    local service=$2
    if nc -z localhost $port 2>/dev/null; then
        echo "✅ $service is running (port $port)"
        return 0
    else
        echo "❌ $service is not accessible (port $port)"
        return 1
    fi
}

# Function to check HTTP endpoint
check_http() {
    local url=$1
    local service=$2
    if curl -sf "$url" > /dev/null 2>&1; then
        echo "✅ $service is healthy ($url)"
        return 0
    else
        echo "❌ $service is not responding ($url)"
        return 1
    fi
}

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi

# Check if containers are running
echo "📦 Checking Docker containers..."
if docker-compose ps | grep -q "Up"; then
    echo "✅ Docker containers are running"
else
    echo "❌ Docker containers are not running"
    echo "   Run: docker-compose up -d"
    exit 1
fi

echo ""
echo "🔍 Checking services..."

# Check PostgreSQL
check_port 5432 "PostgreSQL"

# Check Redis
check_port 6379 "Redis"

# Check Backend
check_port 8000 "Backend API"
if [ $? -eq 0 ]; then
    check_http "http://localhost:8000/health" "Backend Health"
fi

# Check Frontend
check_port 3000 "Frontend"

echo ""
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "💾 Disk Usage:"
docker system df

echo ""
echo "🔗 Access URLs:"
echo "   Frontend:    http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs:    http://localhost:8000/api/docs"
echo ""
