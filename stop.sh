#!/bin/bash
# SBML Builder - Shutdown Script (Linux/Mac)

echo "========================================"
echo " Stopping SBML Builder Services"
echo "========================================"
echo ""

docker-compose down

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo " All services stopped successfully"
    echo "========================================"
    echo ""
else
    echo ""
    echo "ERROR: Failed to stop services"
    echo ""
    exit 1
fi
