@echo off
REM SBML Builder - Zero Auth Edition
REM Windows Startup Script

echo ========================================
echo  SBML Builder - Zero Auth Edition
echo ========================================
echo.
echo Starting 4 Docker services...
echo   - ccapp (SBML Engine)
echo   - app (Java Simulation)
echo   - db (PostgreSQL)
echo   - api (Flask API)
echo.
echo NO AUTHENTICATION REQUIRED
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Start services
echo Building and starting services...
docker-compose up -d --build

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start services!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Services Started Successfully!
echo ========================================
echo.
echo  Access Points:
echo    Builder UI:  http://localhost:5001
echo    API:         http://localhost:5001/api
echo    ccapp:       http://localhost:8082 (internal)
echo    Java Sim:    http://localhost:8081 (internal)
echo    PostgreSQL:  localhost:5432
echo.
echo  NO LOGIN REQUIRED - Direct Access
echo.
echo  To view logs:    docker-compose logs -f
echo  To stop:         stop.bat
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul

REM Open browser
start http://localhost:5001

echo.
echo Press any key to exit (services will keep running)...
pause >nul
