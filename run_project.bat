@echo off
echo ===================================================
echo 🚀 Starting Stock Prediction Project (Full Stack)
echo ===================================================

:: Start Backend
echo.
echo [1/2] Starting Backend (FastAPI)...
start "Backend Server" cmd /k "cd backend && .venv\Scripts\activate && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

:: Start Frontend
echo.
echo [2/2] Starting Frontend (React)...
echo This may take a moment to compile...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo ✅ Servers are starting!
echo ---------------------------------------------------
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo ---------------------------------------------------
echo.
echo Press any key to close this launcher (servers will keep running)...
pause >nul
