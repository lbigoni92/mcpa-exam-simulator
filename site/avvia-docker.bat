@echo off
rem Avvia il simulatore MCPA con Docker (richiede Docker Desktop avviato)
cd /d "%~dp0"
docker compose up -d --build
if errorlevel 1 (
  echo.
  echo Docker non risponde: avvia Docker Desktop e riprova.
  pause
  exit /b 1
)
echo Simulatore attivo su http://localhost:8765/
start "" http://localhost:8765/
timeout /t 3 >nul
