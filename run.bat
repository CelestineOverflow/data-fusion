@echo off
echo Starting API...
cd api
set PORT=5000
set BROWSER=chrome
set DELAY_SECONDS=7 
start /b cmd /c python main.py
start /b cmd /c python camera.py

echo Waiting for API to start...

cd ..
echo Starting Frontend...
cd viewer
start cmd /k npm run dev
