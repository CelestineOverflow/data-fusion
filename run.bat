@echo off
echo Starting API...
cd api
set PORT=5000
set BROWSER=chrome
set DELAY_SECONDS=7 
start /b cmd /c python -m uvicorn main:app --port %PORT% 

cd ..
echo Starting Frontend...
cd viewer
start cmd /k npm run dev
