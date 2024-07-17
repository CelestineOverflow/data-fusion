@echo off
echo Starting API...
cd api
start /b cmd /c python t.py
start /b cmd /c python camera.py