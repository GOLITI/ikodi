# GriotKnowledge 🥁

**Archivage Sémantique RAG du Patrimoine Culturel Ivoirien**

Système de Retrieval-Augmented Generation (RAG) pour préserver et rendre accessible la sagesse ancestrale des peuples de Côte d'Ivoire à travers contes, proverbes et légendes.

---

## 🏗️ Architecture Microservices

```
┌─────────────────────────────────────────────────┐
│              Frontend (React/Vue)               │
└──────────────────┬──────────────────────────────┘
                   │ HTTP/REST
┌──────────────────▼──────────────────────────────┐
│           FastAPI (Port 8000)                   │
│  ┌──────────────────────────────────────────┐   │
│  │  Orchestrator (RAG Pipeline)            │   │
│  │  ┌────────────┐      ┌─────────────┐    │   │
│  │  │ Retriever  │  →   │ LLM (OpenR) │    │   │
│  │  │ (Embeddings│      │             │    │   │
│  │  └─────┬──────┘      └─────────────┘    │   │
│  │        │                                 │   │
│  │  ┌─────▼──────┐                          │   │
│  │  │ Vectorizer │                          │   │
│  │  └─────┬──────┘                          │   │
│  └────────┼─────────────────────────────────┘   │
└───────────┼──────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────┐
│        Qdrant VectorDB (Port 6333)              │
│        Dashboard UI (Port 6335)                  │
└──────────────────────────────────────────────────┘
```

---

## 🚀 Déploiement Rapide

### Prérequis
- Docker & Docker Compose
- 4GB RAM minimum
- Clé API OpenRouter ([obtenir ici](https://openrouter.ai/keys))

### 1️⃣ Configuration

```bash
# Cloner le projet
git clone <votre-repo>
cd griot-knowledge

# Copier et configurer l'environnement
cp .env.example .env

# Éditer .env et ajouter votre clé OpenRouter
nano .env  # ou code .env
```

**Variables critiques à configurer :**
```env
OPENROUTER_API_KEY=sk-or-v1-VOTRE_CLE_ICI
LLM_MODEL=stepfun/step-3.5-flash:free
CORS_ORIGINS=https://votre-domaine.com
DEBUG=false
```

### 2️⃣ Lancement

```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier les logs
docker-compose logs -f api

# Vérifier la santé
curl http://localhost:8000/health
```

### 3️⃣ Ingestion du Corpus

```bash
# Depuis la machine hôte
docker exec -it griot_api python scripts/ingest.py

# Vérifier l'ingestion
curl http://localhost:8000/stats
```

---

## 📡 API Endpoints

### Question RAG Complète
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Comment résoudre un conflit selon la tradition ivoirienne ?",
    "nb_resultats": 3
  }'
```

### Recherche Sémantique
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "question": "sagesse sur la patience",
    "nb_resultats": 5,
    "filtre_ethnie": "baoulé"
  }'
```

### Documentation Interactive
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

---

## 🛡️ Sécurité Production

### ✅ Implémenté
- ✅ Containerisation Docker
- ✅ Utilisateur non-root
- ✅ Health checks automatiques
- ✅ Logging structuré
- ✅ CORS configurable
- ✅ Gestion secrets via .env
- ✅ Limitations ressources

### ⚠️ À Ajouter (selon besoins)
- Rate limiting (slowapi)
- Authentification JWT
- HTTPS/TLS (reverse proxy)
- Monitoring (Prometheus)
- Backup automatique Qdrant

---

## 📊 Monitoring

### Dashboards Disponibles
- **Qdrant UI** : http://localhost:6335
- **API Health** : http://localhost:8000/health
- **API Stats** : http://localhost:8000/stats

### Logs
```bash
# Logs API
docker-compose logs -f api

# Logs Qdrant
docker-compose logs -f qdrant

# Métriques système
docker stats griot_api griot_qdrant
```

---

## 🔧 Développement Local

```bash
# Sans Docker
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Démarrer Qdrant seul
docker-compose up qdrant -d

# Lancer l'API en dev
uvicorn app.main:app --reload
```

---

## 📁 Structure Projet

```
griot-knowledge/
├── app/
│   ├── main.py           # API FastAPI
│   ├── models.py         # Schémas Pydantic
│   ├── orchestrator.py   # Pipeline RAG + LLM
│   ├── retriever.py      # Recherche sémantique
│   └── vectorizer.py     # Embeddings + Qdrant
├── scripts/
│   └── ingest.py         # Ingestion corpus
├── data/
│   └── corpus/           # JSON contes/proverbes
├── Dockerfile            # Image production
├── docker-compose.yml    # Orchestration services
├── requirements.txt      # Dépendances Python
└── .env.example          # Template configuration
```

---

## 🌍 Technologies

| Composant | Technologie | Version |
|-----------|------------|---------|
| **API** | FastAPI | 0.133.1 |
| **LLM** | OpenRouter | - |
| **Embeddings** | Sentence Transformers | 5.2.3 |
| **VectorDB** | Qdrant | 1.17.0 |
| **Orchestration** | LangChain | 1.2.10 |
| **Runtime** | Python | 3.13 |

---

## 📝 License

Projet IvoirIA - Préservation du Patrimoine Culturel Ivoirien

---

## 🤝 Contribution

Pour ajouter du contenu culturel :
1. Créer un fichier JSON dans `data/corpus/`
2. Suivre le schéma `DocumentSource`
3. Lancer `python scripts/ingest.py`

Pour le code :
1. Fork le projet
2. Créer une branche feature
3. Tester avec `pytest`
4. Pull Request

---

## 📞 Support

- **Issues** : GitHub Issues
- **Docs** : `/docs` endpoint
- **Email** : contact@ivoiria.ci
