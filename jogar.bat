@echo off
rem Clique duas vezes neste arquivo para abrir o jogo.
cd /d "%~dp0"
if exist "%USERPROFILE%\anaconda3\python.exe" (
    "%USERPROFILE%\anaconda3\python.exe" main.py
) else (
    python main.py
)
if errorlevel 1 pause
