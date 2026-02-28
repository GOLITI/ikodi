from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

load_dotenv()

from app.routers import niveau1, niveau2, niveau3
from app.services.rag_service import rag_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[STARTUP] Demarrage du Microservice Apprentissage Dioula...")
    try:
        rag_service.initialize()
    except Exception as e:
        print(f"[WARNING] RAG en mode degrade: {e}")
    yield
    print("[SHUTDOWN] Arret du microservice")


app = FastAPI(
    title="🎓 Microservice Apprentissage Dioula",
    description="""
API pour l'apprentissage de la langue **Dioula (Dyula)** — Culture Ivoirienne 🇨🇮

## 📚 Niveaux disponibles
- **Niveau 1** `/api/niveau1` — Texte + Quiz + Explications IA **(Gemini RAG)**
- **Niveau 2** `/api/niveau2` — Texte + Audio TTS (ElevenLabs)
- **Niveau 3** `/api/niveau3` — Interaction vocale IA (Whisper + Gemini RAG + ElevenLabs)

## 🤖 IA
Moteur : **Google Gemini 2.5 Flash** + **LangChain RAG** + **ChromaDB**

## 📦 Dataset
Corpus **Koumankan4Dyula** — 10 929 paires Dioula-Français (HuggingFace)
    """,
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(niveau1.router)
app.include_router(niveau2.router)
app.include_router(niveau3.router)


@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "Microservice Apprentissage Dioula 🇨🇮",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "niveau1_lessons": "/api/niveau1/lessons",
            "niveau2_audio": "/api/niveau2/audio?text=I+ni+ce",
            "niveau3_chat": "/api/niveau3/text-chat",
            "niveau3_voice": "/api/niveau3/voice-interaction",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }


@app.get("/health", tags=["Root"])
async def health():
    llm_engine = "fallback"
    if rag_service.llm is not None:
        llm_engine = getattr(rag_service.llm, "model", "unknown")
    return {
        "status": "ok",
        "rag_initialized": rag_service._initialized,
        "llm_engine": llm_engine,
        "mode": "full_rag" if rag_service.chain else "fallback_text",
    }