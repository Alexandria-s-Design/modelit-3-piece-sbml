@echo off
REM SBML Builder - Shutdown Script (Windows)

echo ========================================
echo  Stopping SBML Builder Services
echo ========================================
echo.

docker-compose down

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo  All services stopped successfully
    echo ========================================
    echo.
) else (
    echo.
    echo ERROR: Failed to stop services
    echo.
)

pause
