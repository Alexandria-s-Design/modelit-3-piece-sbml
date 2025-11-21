#!/bin/bash
# SBML Builder - Zero Auth Edition
# Linux/Mac Startup Script

echo "========================================"
echo " SBML Builder - Zero Auth Edition"
echo "========================================"
echo ""
echo "Starting 4 Docker services..."
echo "  - ccapp (SBML Engine)"
echo "  - app (Java Simulation)"
echo "  - db (PostgreSQL)"
echo "  - api (Flask API)"
echo ""
echo "NO AUTHENTICATION REQUIRED"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running!"
    echo "Please start Docker and try again."
    exit 1
fi

# Start services
echo "Building and starting services..."
docker-compose up -d --build

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to start services!"
    exit 1
fi

echo ""
echo "========================================"
echo " Services Started Successfully!"
echo "========================================"
echo ""
echo "  Access Points:"
echo "    Builder UI:  http://localhost:5001"
echo "    API:         http://localhost:5001/api"
echo "    ccapp:       http://localhost:8082 (internal)"
echo "    Java Sim:    http://localhost:8081 (internal)"
echo "    PostgreSQL:  localhost:5432"
echo ""
echo "  NO LOGIN REQUIRED - Direct Access"
echo ""
echo "  To view logs:    docker-compose logs -f"
echo "  To stop:         ./stop.sh"
echo ""

# Detect OS and open browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sleep 2
    open http://localhost:5001
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    sleep 2
    xdg-open http://localhost:5001 2>/dev/null || echo "Please open http://localhost:5001 in your browser"
fi

echo ""
echo "Services are running in the background."
echo "Press Ctrl+C to exit (services will keep running)"
echo ""

# Keep script running to show logs
docker-compose logs -f
