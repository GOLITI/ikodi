"""
GriotKnowledge — main.py
==========================
Point d'entrée FastAPI.

Expose le pipeline RAG complet via une API REST.

Endpoints :
    GET  /                      → Info API
    GET  /health                → Santé des services
    POST /ask                   → Question → Réponse culturelle (pipeline complet)
    POST /ask/proverbe          → Questions sur les proverbes uniquement
    POST /ask/conte             → Questions sur les contes uniquement
    POST /search                → Recherche sémantique brute (sans LLM)
    POST /ingest                → Ingérer un nouveau document
    DELETE /document/{doc_id}   → Supprimer un document
    GET  /stats                 → Statistiques de la collection

Lancement :
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

import os
import logging
import json
from contextlib import asynccontextmanager
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional
import time

from app.models import (
    RequeteUtilisateur,
    ReponseGriot,
    ResultatRecherche,
    DocumentSource,
    StatutIngestion,
    TypeContenu,
    Ethnie,
    Langue,
)
from app.orchestrator import Orchestrator
from app.vectorizer import Vectorizer

load_dotenv()

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG    = os.getenv("DEBUG", "false").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# ── Logging structuré ───────────────────────────────────────
logging.basicConfig(
    level=logging.INFO if not DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("griot-knowledge")


# ─────────────────────────────────────────────────────────────
# ÉTAT GLOBAL  (services partagés entre les requêtes)
# ─────────────────────────────────────────────────────────────

class AppState:
    orchestrator: Orchestrator | None = None
    vectorizer:   Vectorizer   | None = None

state = AppState()


# ─────────────────────────────────────────────────────────────
# LIFESPAN  (chargement au démarrage, nettoyage à l'arrêt)
# ─────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise les services au démarrage de l'API."""
    logger.info("🥁 Démarrage de GriotKnowledge API...")

    try:
        state.orchestrator = Orchestrator()
        state.vectorizer   = Vectorizer()
        logger.info("✅ Tous les services sont prêts")
    except Exception as e:
        logger.error(f"❌ Erreur d'initialisation : {e}", exc_info=True)
        raise

    yield

    logger.info("👋 Arrêt de GriotKnowledge API")


# ─────────────────────────────────────────────────────────────
# APPLICATION FASTAPI
# ─────────────────────────────────────────────────────────────

app = FastAPI(
    title="GriotKnowledge API",
    description=(
        "Système RAG de préservation culturelle ivoirienne. "
        "Posez vos questions, recevez des réponses ancrées dans "
        "la sagesse des peuples de Côte d'Ivoire."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Serve the built frontend (if present) so the backend can directly host the SPA.
# The frontend build should be located at ../frontend/dist relative to the backend folder.
try:
    frontend_dist = Path(__file__).resolve().parents[1] / "frontend" / "dist"
    if frontend_dist.exists():
        app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
        logger.info(f"✅ Serving frontend from {frontend_dist}")
    else:
        logger.debug(f"Frontend build not found at {frontend_dist}; not mounted")
except Exception as e:
    logger.error(f"Error while mounting frontend static files: {e}")

# CORS — Limité aux origines autorisées
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Middleware de logging des requêtes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s"
    )
    
    return response


# ─────────────────────────────────────────────────────────────
# SCHÉMAS DE REQUÊTES SUPPLÉMENTAIRES
# ─────────────────────────────────────────────────────────────

class QuestionSimple(BaseModel):
    """Raccourci pour poser une question sans options avancées."""
    question: str = Field(
        min_length=3,
        max_length=1000,
        example="Comment résoudre un conflit familial selon la tradition ivoirienne ?"
    )
    nb_resultats: int = Field(default=3, ge=1, le=10)


class RechercheRequest(BaseModel):
    """Requête de recherche sémantique brute."""
    question: str = Field(min_length=3, max_length=1000)
    nb_resultats: int = Field(default=5, ge=1, le=20)
    filtre_ethnie: Optional[Ethnie]       = None
    filtre_type:   Optional[TypeContenu]  = None


# ─────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────

@app.get("/", tags=["Info"])
async def racine():
    """Informations générales sur l'API."""
    return {
        "nom":         "GriotKnowledge API",
        "version":     "1.0.0",
        "description": "Archivage sémantique RAG du patrimoine culturel ivoirien",
        "projet":      "IvoirIA",
        "endpoints": {
            "ask":       "POST /ask             → Question complète avec réponse LLM",
            "ask_conte": "POST /ask/conte       → Questions sur les contes uniquement",
            "ask_prov":  "POST /ask/proverbe    → Questions sur les proverbes uniquement",
            "search":    "POST /search          → Recherche sémantique brute",
            "ingest":    "POST /ingest          → Ajouter un document au corpus",
            "stats":     "GET  /stats           → Statistiques de la collection",
            "docs":      "GET  /docs            → Documentation interactive Swagger",
        }
    }


@app.get("/health", tags=["Info"])
async def health():
    """Vérifie l'état des services (Qdrant, LLM, Embedding)."""
    from qdrant_client import QdrantClient
    checks = {}

    # Qdrant
    try:
        client = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333))
        )
        info = client.get_collection(os.getenv("QDRANT_COLLECTION_NAME", "griot_corpus"))
        nb = info.points_count
        checks["qdrant"] = {"status": "ok", "nb_vecteurs": nb}
        logger.debug(f"Qdrant health check: {nb} vecteurs")
    except Exception as e:
        logger.error(f"Qdrant health check failed: {e}")
        checks["qdrant"] = {"status": "error", "detail": str(e)[:100]}

    # Orchestrator
    checks["orchestrator"] = {
        "status": "ok" if state.orchestrator else "non initialisé",
        "llm":    type(state.orchestrator.llm).__name__ if state.orchestrator else "N/A",
    }

    tout_ok = all(v.get("status") == "ok" for v in checks.values())
    return {"status": "healthy" if tout_ok else "degraded", "services": checks}


@app.post("/ask", response_model=ReponseGriot, tags=["RAG"])
async def poser_question(requete: RequeteUtilisateur):
    """
    **Pipeline RAG complet.**

    Pose une question et reçoit une réponse générée par le LLM,
    ancrée sur les contes et proverbes ivoiriens du corpus.

    - `question` : votre question en français
    - `filtre_ethnie` : limiter à une ethnie (baoulé, dioula, sénoufo...)
    - `filtre_type` : limiter à conte ou proverbe
    - `nb_resultats` : nombre de sources à utiliser (1-10)
    """
    if not state.orchestrator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator non initialisé"
        )
    try:
        reponse = state.orchestrator.repondre(requete)
        return reponse
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération : {str(e)}"
        )


@app.post("/ask/simple", response_model=ReponseGriot, tags=["RAG"])
async def question_simple(body: QuestionSimple):
    """
    **Raccourci — question simple sans options avancées.**

    Idéal pour les intégrations rapides.
    """
    if not state.orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator non initialisé")

    requete = RequeteUtilisateur(
        question=body.question,
        nb_resultats=body.nb_resultats,
    )
    return state.orchestrator.repondre(requete)


@app.post("/ask/proverbe", response_model=ReponseGriot, tags=["RAG"])
async def question_proverbe(body: QuestionSimple):
    """
    **Question sur les proverbes uniquement.**

    Retourne uniquement des réponses basées sur les proverbes ivoiriens.
    Filtre automatiquement les contes.
    """
    if not state.orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator non initialisé")

    requete = RequeteUtilisateur(
        question=body.question,
        nb_resultats=body.nb_resultats,
        filtre_type=TypeContenu.PROVERBE,
    )
    return state.orchestrator.repondre(requete)


@app.post("/ask/conte", response_model=ReponseGriot, tags=["RAG"])
async def question_conte(body: QuestionSimple):
    """
    **Question sur les contes uniquement.**

    Retourne uniquement des réponses basées sur les contes traditionnels ivoiriens.
    Filtre automatiquement les proverbes.
    """
    if not state.orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator non initialisé")

    requete = RequeteUtilisateur(
        question=body.question,
        nb_resultats=body.nb_resultats,
        filtre_type=TypeContenu.CONTE,
    )
    return state.orchestrator.repondre(requete)


@app.post("/search", response_model=list[ResultatRecherche], tags=["Recherche"])
async def recherche_semantique(body: RechercheRequest):
    """
    **Recherche sémantique brute.**

    Retourne les documents les plus proches sémantiquement,
    sans passer par le LLM. Utile pour explorer le corpus.
    """
    if not state.orchestrator:
        raise HTTPException(status_code=503, detail="Service non initialisé")

    try:
        resultats = state.orchestrator.retriever.rechercher(
            question=body.question,
            nb_resultats=body.nb_resultats,
            filtre_ethnie=body.filtre_ethnie,
            filtre_type=body.filtre_type,
        )
        return resultats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/ingest",
    response_model=StatutIngestion,
    status_code=status.HTTP_201_CREATED,
    tags=["Corpus"],
)
async def ingerer_document(doc: DocumentSource):
    """
    **Ajouter un nouveau document au corpus.**

    Indexe un conte ou proverbe et le rend immédiatement
    disponible pour la recherche sémantique.
    """
    if not state.vectorizer:
        # Créer un vectorizer si pas encore initialisé
        state.vectorizer = Vectorizer()

    try:
        resultat = state.vectorizer.indexer_document(doc)
        return StatutIngestion(
            documents_traites=1,
            chunks_crees=resultat["chunks"],
            vecteurs_stockes=resultat["vecteurs"],
            succes=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/document/{doc_id}", tags=["Corpus"])
async def supprimer_document(doc_id: str):
    """
    **Supprimer un document du corpus.**

    Supprime tous les chunks associés au `doc_id` dans Qdrant.
    """
    if not state.vectorizer:
        state.vectorizer = Vectorizer()

    try:
        state.vectorizer.supprimer_document(doc_id)
        return {"message": f"Document '{doc_id}' supprimé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", tags=["Corpus"])
async def statistiques():
    """
    **Statistiques de la collection Qdrant.**

    Retourne le nombre de vecteurs, la dimension et la métrique utilisée.
    """
    if not state.vectorizer:
        state.vectorizer = Vectorizer()

    try:
        return state.vectorizer.stats_collection()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────
# LANCEMENT DIRECT  (python app/main.py)
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG,
    )