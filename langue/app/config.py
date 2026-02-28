"""
Configuration file for the Dioula Microservice
Handles environment variables and application settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ── API Keys ──────────────────────────────────────────────
MISTRAL_API_KEY     = os.getenv("MISTRAL_API_KEY", "")       # Mistral API key
GOOGLE_API_KEY      = os.getenv("GEMINI_KEY", "")           # Gemini API key (embeddings)
ELEVENLABS_API_KEY  = os.getenv("ELEVENLABS_API_KEY", "")
HUGGINGFACE_TOKEN   = os.getenv("HUGGINGFACE_TOKEN", "")

# ── Application Settings ──────────────────────────────────
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
HOST  = os.getenv("HOST", "0.0.0.0")
PORT  = int(os.getenv("PORT", "8001"))

# ── LLM Model Settings ────────────────────────────────────
LLM_PROVIDER        = os.getenv("LLM_PROVIDER", "mistral")  # mistral | gemini
MISTRAL_MODEL       = os.getenv("MISTRAL_MODEL", "mistral-small-latest")
GEMINI_LLM_MODEL    = os.getenv("GEMINI_LLM_MODEL",   "gemini-2.5-flash")
GEMINI_EMBED_MODEL  = os.getenv("GEMINI_EMBED_MODEL",  "models/gemini-embedding-001")
LLM_TEMPERATURE     = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_MAX_TOKENS      = int(os.getenv("LLM_MAX_TOKENS",    "512"))

# ── Whisper STT Settings ──────────────────────────────────
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")  # base | small | medium

# ── ElevenLabs TTS Settings ───────────────────────────────
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

# ── HuggingFace Dataset ───────────────────────────────────
DATASET_NAME    = os.getenv("DATASET_NAME",  "uvci/Koumankan_mt_dyu_fr")
DATASET_SPLIT   = os.getenv("DATASET_SPLIT", "train")
DATASET_SIZE    = int(os.getenv("DATASET_SIZE", "800"))

# ── RAG Settings ──────────────────────────────────────────
K_DOCUMENTS      = int(os.getenv("K_DOCUMENTS",   "5"))     # nb docs récupérés
SCORE_THRESHOLD  = float(os.getenv("SCORE_THRESHOLD", "0.7"))  # seuil quiz correct
CHUNK_SIZE       = int(os.getenv("CHUNK_SIZE",    "500"))
CHUNK_OVERLAP    = int(os.getenv("CHUNK_OVERLAP", "50"))


def validate_config() -> dict:
    """
    Vérifie que les clés obligatoires sont présentes.
    Appelée au démarrage dans main.py
    """
    missing = []
    warnings = []

    if LLM_PROVIDER == "mistral" and not MISTRAL_API_KEY:
        missing.append("MISTRAL_API_KEY  (obtenez-la sur console.mistral.ai)")
    if LLM_PROVIDER == "gemini" and not GOOGLE_API_KEY:
        missing.append("GEMINI_KEY  (obtenez-la sur aistudio.google.com — gratuit)")
    if not GOOGLE_API_KEY:
        warnings.append("GEMINI_KEY manquant → embeddings désactivés (fallback)")
    if not ELEVENLABS_API_KEY:
        warnings.append("ELEVENLABS_API_KEY  manquante → Niveau 2 et 3 audio désactivés")
    if not HUGGINGFACE_TOKEN:
        warnings.append("HUGGINGFACE_TOKEN  manquant → dataset de fallback (50 phrases) utilisé")

    return {
        "missing":  missing,
        "warnings": warnings,
        "valid":    len(missing) == 0,
    }