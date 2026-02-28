# 🔌 API Endpoints pour le Frontend

**Base URL** : `http://localhost:8000` (dev) ou `https://api.griot-knowledge.com` (prod)

---

## 📍 **Endpoints Essentiels**

### 1️⃣ **Poser une Question (Principal)**
**Le plus important pour votre frontend**

```http
POST /ask/simple
Content-Type: application/json
```

**Request Body :**
```json
{
  "question": "Comment résoudre un conflit familial ?",
  "nb_resultats": 3
}
```

**Response :**
```json
{
  "question": "Comment résoudre un conflit familial ?",
  "reponse": "D'après le proverbe bété sur le conflit, la sagesse ivoirienne enseigne que...",
  "sources": [
    {
      "chunk_id": "xyz",
      "doc_id": "baou_prov_001",
      "titre_parent": "Proverbe sur le conflit",
      "contenu": "Les conflits entre puissants...",
      "ethnie": "baoulé",
      "type_contenu": "proverbe",
      "score": 0.8542,
      "morale": "La paix vaut mieux que la victoire"
    }
  ],
  "nb_sources": 1,
  "langue_reponse": "fr"
}
```

**Utilisation Frontend :**
```javascript
// React/Vue/Angular
async function askQuestion(userQuestion) {
  const response = await fetch('http://localhost:8000/ask/simple', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      question: userQuestion,
      nb_resultats: 3
    })
  });
  return await response.json();
}
```

---

### 2️⃣ **Questions sur les Proverbes uniquement**
Filtre automatiquement pour ne retourner que des proverbes

```http
POST /ask/proverbe
Content-Type: application/json
```

**Request Body :**
```json
{
  "question": "Comment gérer la patience ?",
  "nb_resultats": 3
}
```

**Response :**
```json
{
  "question": "Comment gérer la patience ?",
  "reponse": "Selon les proverbes ivoiriens sur la patience...",
  "sources": [
    {
      "doc_id": "ci_prov_042",
      "titre_parent": "Proverbe sur la patience",
      "contenu": "La patience est un arbre...",
      "ethnie": "baoulé",
      "type_contenu": "proverbe",
      "score": 0.8234
    }
  ]
}
```

**Utilisation Frontend :**
```javascript
async function askProverbe(question) {
  const response = await fetch('http://localhost:8000/ask/proverbe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, nb_resultats: 3 })
  });
  return await response.json();
}
```

---

### 3️⃣ **Questions sur les Contes uniquement**
Filtre automatiquement pour ne retourner que des contes

```http
POST /ask/conte
Content-Type: application/json
```

**Request Body :**
```json
{
  "question": "Raconte-moi une histoire sur le courage",
  "nb_resultats": 3
}
```

**Response :**
```json
{
  "question": "Raconte-moi une histoire sur le courage",
  "reponse": "D'après le conte yacouba 'Yakouba et le Lion'...",
  "sources": [
    {
      "doc_id": "yacouba_conte_002",
      "titre_parent": "Yakouba et le Lion",
      "contenu": "Yakouba était un jeune garçon...",
      "ethnie": "yacouba",
      "type_contenu": "conte",
      "score": 0.7845,
      "morale": "Le vrai courage est de savoir renoncer"
    }
  ]
}
```

**Utilisation Frontend :**
```javascript
async function askConte(question) {
  const response = await fetch('http://localhost:8000/ask/conte', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, nb_resultats: 3 })
  });
  return await response.json();
}
```

---

### 5️⃣ **Recherche Sémantique (Optionnel)**
Trouver des documents sans générer de réponse LLM

```http
POST /search
Content-Type: application/json
```

**Request Body :**
```json
{
  "question": "sagesse sur la patience",
  "nb_resultats": 5,
  "filtre_ethnie": "baoulé",
  "filtre_type": "conte"
}
```

**Response :**
```json
[
  {
    "chunk_id": "abc123",
    "doc_id": "baou_conte_002",
    "titre_parent": "La tortue et l'aigle",
    "contenu": "Il était une fois...",
    "ethnie": "baoulé",
    "type_contenu": "conte",
    "score": 0.7234,
    "morale": "La persévérance ouvre des portes..."
  }
]
```

**Filtres disponibles :**
- `filtre_ethnie` : `"baoulé"` | `"dioula"` | `"sénoufo"` | `"bété"` | `"agni"` | etc.
- `filtre_type` : `"conte"` | `"proverbe"` | `"legende"` | `"chant"` | `"rituel"`

---

### 6️⃣ **Statistiques du Corpus**
Afficher nombre de documents indexés

```http
GET /stats
```

**Response :**
```json
{
  "collection": "griot_corpus",
  "nb_vecteurs": 42,
  "dimension": 384,
  "distance": "Cosine"
}
```

**Utilisation Frontend :**
```javascript
// Afficher dans le footer ou dashboard
async function getStats() {
  const response = await fetch('http://localhost:8000/stats');
  const stats = await response.json();
  console.log(`${stats.nb_vecteurs} documents indexés`);
}
```

---

### 7️⃣ **Health Check**
Vérifier que l'API est opérationnelle

```http
GET /health
```

**Response :**
```json
{
  "status": "healthy",
  "services": {
    "qdrant": {
      "status": "ok",
      "nb_vecteurs": 42
    },
    "orchestrator": {
      "status": "ok",
      "llm": "ChatOpenAI"
    }
  }
}
```

---

### 8️⃣ **Informations API**
Métadonnées et version

```http
GET /
```

**Response :**
```json
{
  "nom": "GriotKnowledge API",
  "version": "1.0.0",
  "description": "Archivage sémantique RAG du patrimoine culturel ivoirien",
  "endpoints": {
    "ask": "POST /ask/simple",
    "search": "POST /search",
    "stats": "GET /stats"
  }
}
```

---

## 🎨 **Exemples d'Intégration Frontend**

### **React (TypeScript)**

```tsx
import { useState } from 'react';

interface GriotResponse {
  question: string;
  reponse: string;
  sources: Array<{
    titre_parent: string;
    ethnie: string;
    type_contenu: string;
    score: number;
  }>;
}

function ChatBot() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState<GriotResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    setLoading(true);
    const res = await fetch('http://localhost:8000/ask/simple', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, nb_resultats: 3 })
    });
    const data = await res.json();
    setResponse(data);
    setLoading(false);
  };

  return (
    <div>
      <input 
        value={question} 
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Posez votre question..."
      />
      <button onClick={handleAsk} disabled={loading}>
        {loading ? 'Réflexion...' : 'Demander au Griot'}
      </button>
      
      {response && (
        <div>
          <p>{response.reponse}</p>
          <h4>Sources ({response.nb_sources}):</h4>
          {response.sources.map((src, i) => (
            <div key={i}>
              <strong>{src.titre_parent}</strong> ({src.ethnie})
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

---

### **Vue 3 (Composition API)**

```vue
<script setup>
import { ref } from 'vue';

const question = ref('');
const response = ref(null);
const loading = ref(false);

async function askGriot() {
  loading.value = true;
  const res = await fetch('http://localhost:8000/ask/simple', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      question: question.value,
      nb_resultats: 3 
    })
  });
  response.value = await res.json();
  loading.value = false;
}
</script>

<template>
  <div>
    <input v-model="question" placeholder="Question..." />
    <button @click="askGriot" :disabled="loading">
      Demander
    </button>
    
    <div v-if="response">
      <p>{{ response.reponse }}</p>
      <div v-for="(src, i) in response.sources" :key="i">
        {{ src.titre_parent }}
      </div>
    </div>
  </div>
</template>
```

---

### **Vanilla JavaScript**

```javascript
async function askGriot(question) {
  const response = await fetch('http://localhost:8000/ask/simple', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, nb_resultats: 3 })
  });
  
  const data = await response.json();
  
  // Afficher réponse
  document.getElementById('answer').textContent = data.reponse;
  
  // Afficher sources
  const sourcesList = document.getElementById('sources');
  sourcesList.innerHTML = data.sources.map(src => 
    `<li><strong>${src.titre_parent}</strong> (${src.ethnie})</li>`
  ).join('');
}
```

---

## 🔐 **CORS et Sécurité**

Votre frontend doit être autorisé dans `.env` :

```env
CORS_ORIGINS=http://localhost:3000,https://votre-domaine.com
```

Si vous avez une erreur CORS :
1. Vérifiez que votre domaine est dans `CORS_ORIGINS`
2. Redémarrez l'API après modification `.env`

---

## 📊 **Gestion des Erreurs**

```javascript
async function askGriot(question) {
  try {
    const response = await fetch('http://localhost:8000/ask/simple', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, nb_resultats: 3 })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
    
  } catch (error) {
    console.error('Erreur API:', error);
    return {
      question,
      reponse: "Le griot est temporairement indisponible. Veuillez réessayer.",
      sources: [],
      nb_sources: 0
    };
  }
}
```

---

## 🎯 **Endpoints à Utiliser Selon Usage**

| Use Case | Endpoint | Usage |
|----------|----------|-------|
| **Chat conversationnel** | `POST /ask/simple` | ⭐ Principal |
| **Recherche de contes** | `POST /search` | Avec filtres ethnie/type |
| **Dashboard stats** | `GET /stats` | Afficher nb documents |
| **Monitoring** | `GET /health` | Vérifier disponibilité |

---

## 📝 **Documentation Interactive**

Une fois l'API lancée, accédez à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

Vous pouvez **tester les endpoints directement** dans le navigateur !

---

## 🚀 **Résumé pour Démarrer**

**Endpoint minimum viable pour le frontend :**

```javascript
const API_URL = 'http://localhost:8000';

export async function askQuestion(question) {
  const response = await fetch(`${API_URL}/ask/simple`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, nb_resultats: 3 })
  });
  return await response.json();
}
```

C'est tout ce dont vous avez besoin pour commencer ! 🎉
