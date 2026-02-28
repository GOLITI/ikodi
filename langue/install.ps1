# Installation script for Dioula Microservice
Write-Host "Creating virtual environment with Python 3.12..." -ForegroundColor Green
& "C:\Users\fofan\AppData\Local\Programs\Python\Python312\python.exe" -m venv .venv --without-pip

Write-Host "Bootstrapping pip..." -ForegroundColor Green
.\.venv\Scripts\python.exe -m ensurepip

Write-Host "Upgrading pip, setuptools, and wheel..." -ForegroundColor Green
.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel

Write-Host "Installing core dependencies..." -ForegroundColor Green
.\.venv\Scripts\python.exe -m pip install fastapi uvicorn[standard] python-dotenv

Write-Host "Installing LangChain and AI dependencies..." -ForegroundColor Green
.\.venv\Scripts\python.exe -m pip install langchain langchain-community langchain-google-genai google-generativeai

Write-Host "Installing vector store..." -ForegroundColor Green
.\.venv\Scripts\python.exe -m pip install chromadb

Write-Host "Installing HuggingFace tools..." -ForegroundColor Green
.\.venv\Scripts\python.exe -m pip install datasets huggingface-hub

Write-Host "Installing TTS/STT..." -ForegroundColor Green
.\.venv\Scripts\python.exe -m pip install elevenlabs openai-whisper

Write-Host "Installing FastAPI utilities..." -ForegroundColor Green
.\.venv\Scripts\python.exe -m pip install python-multipart httpx pydantic

Write-Host "`nInstallation complete!" -ForegroundColor Green
Write-Host "Activate the environment with: .venv\Scripts\activate" -ForegroundColor Yellow
