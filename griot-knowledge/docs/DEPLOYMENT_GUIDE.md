# Guide de Déploiement - GriotKnowledge

## Architecture du Système

```
┌──────────────────────────────────────────────────────────────┐
│                    FRONTEND                                   │
│            (React, Vue, Angular, etc.)                        │
│               Port: 3000 (dev) / 80 (prod)                    │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        │ HTTP/REST API
                        │ CORS: localhost:3000, votre-domaine.com
                        ↓
┌──────────────────────────────────────────────────────────────┐
│                  BACKEND - FastAPI                            │
│                   Port: 8000                                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Endpoints REST                                     │     │
│  │  - POST /ask/simple     → RAG complet               │     │
│  │  - POST /ask            → RAG avec filtres          │     │
│  │  - POST /search         → Recherche sémantique      │     │
│  │  - GET  /stats          → Statistiques              │     │
│  │  - GET  /health         → Health check              │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Orchestrator (orchestrator.py)                     │     │
│  │    │                                                │     │
│  │    ├─→ OpenRouter API (LLM externe)                │     │
│  │    │     stepfun/step-3.5-flash:free               │     │
│  │    │                                                │     │
│  │    └─→ Retriever (retriever.py)                    │     │
│  │          │                                          │     │
│  │          └─→ Vectorizer (vectorizer.py)            │     │
│  │                Sentence Transformers               │     │
│  └────────────────────────────────────────────────────┘     │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ↓
              ┌─────────────────────┐
              │   Qdrant VectorDB    │
              │    Port: 6333        │
              │  18 vecteurs (384d)  │
              └─────────────────────┘
```

---

## Installation et Déploiement

### Option 1 : Déploiement Docker (Recommandé)

**Prérequis :**
- Docker Desktop installé
- Docker Compose installé
- Clé API OpenRouter (gratuite sur openrouter.ai)

**Étapes :**

```powershell
# 1. Cloner le projet
cd C:\hackaton\griot-knowledge

# 2. Configurer les variables d'environnement
cp .env.example .env

# Éditer .env et ajouter :
# OPENROUTER_API_KEY=sk-or-v1-votre-cle-ici
# LLM_MODEL=stepfun/step-3.5-flash:free
# CORS_ORIGINS=http://localhost:3000,https://votre-domaine.com

# 3. Construire et démarrer les services
docker-compose up -d --build

# 4. Vérifier le statut
docker-compose ps

# 5. Voir les logs
docker logs griot_api -f
docker logs griot_qdrant -f

# 6. Ingérer le corpus initial
docker exec -it griot_api python scripts/ingest.py

# 7. Tester l'API
curl http://localhost:8000/health
curl http://localhost:8000/stats
```

**Gestion des services :**
```powershell
# Arrêter
docker-compose down

# Redémarrer
docker-compose restart

# Voir les logs
docker-compose logs -f api

# Supprimer tout (données incluses)
docker-compose down -v
```

---

### Option 2 : Déploiement Manuel (Dev)

```powershell
# 1. Installer Python 3.11+
python --version

# 2. Créer environnement virtuel
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Démarrer Qdrant (Docker)
docker run -d -p 6333:6333 -p 6334:6334 -v qdrant_data:/qdrant/storage qdrant/qdrant:v1.17.0

# 5. Configurer .env
cp .env.example .env
# Éditer .env avec votre clé API

# 6. Démarrer l'API
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 7. Ingérer les données
python scripts/ingest.py
```

---

## Configuration Frontend

### Variables d'environnement Frontend

Créer un fichier `.env` dans votre projet frontend :

```env
# React (.env)
REACT_APP_API_URL=http://localhost:8000

# Vue (.env)
VITE_API_URL=http://localhost:8000

# Next.js (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

### Exemple : Intégration React

```javascript
// src/services/griotApi.js
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const griotApi = {
  // Poser une question simple
  async askSimple(question) {
    const response = await fetch(`${API_URL}/ask/simple`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    return response.json();
  },

  // Question avec filtres
  async ask(question, filters = {}) {
    const response = await fetch(`${API_URL}/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question,
        nb_resultats: filters.nb_resultats || 3,
        filtre_ethnie: filters.ethnie,
        filtre_type: filters.type,
      }),
    });
    
    return response.json();
  },

  // Recherche sémantique
  async search(query, filters = {}) {
    const response = await fetch(`${API_URL}/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question: query,
        nb_resultats: filters.nb_resultats || 5,
        filtre_ethnie: filters.ethnie,
        filtre_type: filters.type,
      }),
    });
    
    return response.json();
  },

  // Statistiques
  async getStats() {
    const response = await fetch(`${API_URL}/stats`);
    return response.json();
  },

  // Health check
  async getHealth() {
    const response = await fetch(`${API_URL}/health`);
    return response.json();
  },
};
```

**Utilisation dans un composant React :**

```javascript
// src/components/GriotChat.jsx
import React, { useState } from 'react';
import { griotApi } from '../services/griotApi';

export default function GriotChat() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await griotApi.askSimple(question);
      setResponse(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="griot-chat">
      <h1>Griot - Sagesse Ivoirienne</h1>
      
      <form onSubmit={handleSubmit}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Posez votre question..."
          rows={4}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Réflexion...' : 'Demander au Griot'}
        </button>
      </form>

      {error && (
        <div className="error">Erreur : {error}</div>
      )}

      {response && (
        <div className="response">
          <h2>Réponse :</h2>
          <p style={{ whiteSpace: 'pre-wrap' }}>{response.reponse}</p>

          <h3>Sources ({response.nb_sources}) :</h3>
          <ul>
            {response.sources.map((source, idx) => (
              <li key={idx}>
                <strong>{source.titre_parent}</strong> ({source.ethnie})
                <br />
                <em>Score : {source.score}</em>
                <br />
                {source.morale && <span>Morale : {source.morale}</span>}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
```

---

### Exemple : Intégration Vue 3

```javascript
// src/composables/useGriotApi.js
import { ref } from 'vue';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function useGriotApi() {
  const loading = ref(false);
  const error = ref(null);
  const response = ref(null);

  const askSimple = async (question) => {
    loading.value = true;
    error.value = null;
    
    try {
      const res = await fetch(`${API_URL}/ask/simple`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });
      
      if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
      
      response.value = await res.json();
      return response.value;
    } catch (err) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    error,
    response,
    askSimple,
  };
}
```

---

## Configuration CORS

Le backend est déjà configuré pour accepter les requêtes cross-origin.

**Dans `.env` :**
```env
# Environnement dev
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Production
CORS_ORIGINS=https://votre-domaine.com,https://www.votre-domaine.com
```

**Vérification :**
```javascript
// Test CORS depuis le navigateur
fetch('http://localhost:8000/health')
  .then(res => res.json())
  .then(data => console.log('CORS OK:', data))
  .catch(err => console.error('CORS Error:', err));
```

---

## Déploiement Production

### Option 1 : Docker sur VPS

```bash
# 1. Sur le serveur
git clone https://github.com/votre-repo/griot-knowledge.git
cd griot-knowledge

# 2. Configurer l'environnement
cp .env.example .env
nano .env  # Éditer avec les vraies clés

# 3. Démarrer avec Docker Compose
docker-compose -f docker-compose.yml up -d --build

# 4. Configurer Nginx reverse proxy
sudo nano /etc/nginx/sites-available/griot-api

# Contenu :
server {
    listen 80;
    server_name api.votre-domaine.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# 5. Activer et redémarrer Nginx
sudo ln -s /etc/nginx/sites-available/griot-api /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# 6. HTTPS avec Let's Encrypt
sudo certbot --nginx -d api.votre-domaine.com
```

---

### Option 2 : Cloud (Render, Railway, Fly.io)

**Fichier `render.yaml` (pour Render.com) :**
```yaml
services:
  - type: web
    name: griot-api
    env: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: OPENROUTER_API_KEY
        sync: false
      - key: QDRANT_HOST
        value: qdrant
      - key: QDRANT_PORT
        value: 6333

  - type: pserv
    name: griot-qdrant
    env: docker
    dockerCommand: qdrant/qdrant:v1.17.0
    disk:
      name: qdrant-data
      mountPath: /qdrant/storage
      sizeGB: 10
```

---

## Monitoring et Logs

```powershell
# Logs en temps réel
docker-compose logs -f api

# Logs des 100 dernières lignes
docker-compose logs --tail=100 api

# Métriques des containers
docker stats griot_api griot_qdrant

# Vérifier la santé
curl http://localhost:8000/health
curl http://localhost:8000/stats
```

---

## Troubleshooting

### API ne répond pas
```powershell
# Vérifier que les containers tournent
docker-compose ps

# Redémarrer
docker-compose restart api

# Voir les logs d'erreur
docker logs griot_api --tail=50
```

### Qdrant ne se connecte pas
```powershell
# Vérifier Qdrant
curl http://localhost:6333

# Rebuild
docker-compose down
docker-compose up -d --build
```

### Pas de résultats de recherche
```powershell
# Vérifier les stats
curl http://localhost:8000/stats

# Ré-ingérer le corpus
docker exec -it griot_api python scripts/ingest.py

# Vérifier les logs
docker logs griot_api | grep "Vectorizer"
```

---

## URLs importantes

| Service | URL Dev | URL Prod (exemple) |
|---------|---------|-------------------|
| API | http://localhost:8000 | https://api.griot.com |
| API Docs | http://localhost:8000/docs | https://api.griot.com/docs |
| Qdrant | http://localhost:6333 | Interne uniquement |
| Qdrant UI | http://localhost:6335 | Interne uniquement |
| Frontend | http://localhost:3000 | https://griot.com |

---

## Résumé

✅ **Backend** : FastAPI sur port 8000  
✅ **Database** : Qdrant VectorDB sur port 6333  
✅ **LLM** : OpenRouter API (externe)  
✅ **Frontend** : Consomme `/ask/simple`, `/ask`, `/search`  
✅ **CORS** : Configuré via `.env`  
✅ **Docker** : Tout tourne dans des containers  

**Pour démarrer :**
```powershell
docker-compose up -d --build
docker exec -it griot_api python scripts/ingest.py
# Frontend fait des appels à http://localhost:8000/ask/simple
```
