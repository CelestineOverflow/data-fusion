@echo off
set PORT=5000
set BROWSER=chrome
set DELAY_SECONDS=7 
start /b cmd /c python -m uvicorn main:app --port %PORT% --reload
timeout /t %DELAY_SECONDS% /nobreak > NUL
start %BROWSER% "http://localhost:%PORT%/docs"
