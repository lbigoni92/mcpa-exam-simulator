@echo off
title Simulatore MCPA
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 server.py
  goto :fine
)
where python >nul 2>nul
if %errorlevel%==0 (
  python server.py
  goto :fine
)
echo.
echo Python 3 non trovato su questo PC.
echo Installalo da https://www.python.org/downloads/ (spunta "Add python.exe to PATH")
echo oppure da terminale:  winget install Python.Python.3.12
echo Poi fai di nuovo doppio clic su avvia.bat.
:fine
echo.
pause
