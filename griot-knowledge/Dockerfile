# ============================================
# GriotKnowledge - Dockerfile Multi-Stage
# ============================================

FROM python:3.13.11-slim AS base

# Métadonnées
LABEL maintainer="IvoirIA Team"
LABEL description="GriotKnowledge - Archivage sémantique RAG du patrimoine culturel ivoirien"
LABEL version="1.0.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Répertoire de travail
WORKDIR /app

# Copier requirements et installer les dépendances
# Copier requirements minimal runtime et installer les dépendances
# Use `requirements-runtime.txt` to avoid installing heavy ML packages
COPY requirements-docker.txt ./requirements-docker.txt
RUN pip install --no-cache-dir -r requirements-docker.txt

# Copier le code de l'application
COPY app/ ./app/
COPY scripts/ ./scripts/
COPY data/ ./data/

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 griot && \
    chown -R griot:griot /app

USER griot

# Exposer le port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)"

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
