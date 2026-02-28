# 🎓 API Microservice Apprentissage Dioula - Documentation Frontend

## 📡 Base URL
```
http://127.0.0.1:8001
```

## 🔑 Technologies
- **LLM**: Mistral AI (`mistral-small`)
- **Embeddings**: Mistral Embed (1024 dims)
- **Vector DB**: ChromaDB (500 phrases Dioula-Français)
- **Dataset**: HuggingFace `uvci/Koumankan_mt_dyu_fr`

---

## 📚 NIVEAU 1 — Texte + Quiz + IA

### GET `/api/niveau1/lessons`
Récupère la liste de toutes les leçons.

**Response:**
```json
{
  "total": 6,
  "lessons": [
    {
      "id": 1,
      "title": "Les Salutations",
      "theme": "greetings",
      "emoji": "👋",
      "description": "Apprenez à saluer en Dioula...",
      "phrase_count": 7,
      "quiz_count": 5
    }
  ]
}
```

---

### GET `/api/niveau1/lessons/{lesson_id}`
Récupère le contenu complet d'une leçon (phrases + quiz).

**Response:**
```json
{
  "id": 1,
  "title": "Les Salutations",
  "content": [
    {"dioula": "I ni sogoma", "french": "Bonjour"},
    {"dioula": "I ni ce", "french": "Merci"}
  ],
  "quiz": [
    {
      "id": "q1",
      "question": "Comment dit-on bonjour?",
      "options": ["I ni sogoma", "I ni ce", "A ni wula"],
      "correct": 0
    }
  ]
}
```

---

### GET `/api/niveau1/lessons/{lesson_id}/quiz`
Récupère les questions du quiz **sans révéler les réponses**.

**Response:**
```json
{
  "lesson_id": 1,
  "lesson_title": "Les Salutations",
  "quiz": [
    {
      "id": "q1",
      "question": "Comment dit-on bonjour le matin ?",
      "options": ["I ni sogoma", "I ni wula", "I ni suu"]
    }
  ],
  "total": 5
}
```

---

### POST `/api/niveau1/lessons/{lesson_id}/quiz/check`
Vérifie la réponse d'une question de quiz.

**Request Body:**
```json
{
  "lesson_id": 1,
  "question_id": "q1",
  "answer_index": 0
}
```

**Response:**
```json
{
  "correct": true,
  "correct_index": 0,
  "correct_answer": "I ni sogoma",
  "explanation": "C'est la salutation du matin en Dioula",
  "score_points": 10,
  "encouragement": "I ni baara! Excellent! 🎉"
}
```

---

### POST `/api/niveau1/ask`
Pose une question libre à l'IA Mistral (RAG avec corpus Dioula).

**Request Body:**
```json
{
  "question": "Comment dit-on merci en Dioula?"
}
```

**Response:**
```json
{
  "question": "Comment dit-on merci en Dioula?",
  "answer": "🗣️ En Dioula : I ni ce\n🇫🇷 En Français : Merci\n💡 Conseil : Tu peux personnaliser...",
  "similar_phrases": [
    {"dioula": "I ni ce", "french": "Merci"},
    {"dioula": "An ni ce a ka jabilila", "french": "Merci de votre réponse"}
  ]
}
```

**Usage Frontend:**
- Chatbot pédagogique
- Explications contextuelles
- Recherche dans le corpus

---

### GET `/api/niveau1/search?q={query}&k={limit}`
Recherche sémantique dans le corpus Dioula.

**Query Params:**
- `q` (required): Texte à chercher
- `k` (optional): Nombre de résultats (default: 5, max: 10)

**Response:**
```json
{
  "query": "bonjour",
  "results": [
    {"dioula": "I ni sogoma", "french": "Bonjour"},
    {"dioula": "A ni sɛgɛn", "french": "Bonjour (formel)"}
  ],
  "count": 2
}
```

---

## 🔊 NIVEAU 2 — Texte + Audio (TTS)

### GET `/api/niveau2/phrases`
Récupère la liste des phrases audio pour niveau 2.

**Response:**
```json
[
  {
    "id": 1,
    "dioula": "I ni sogoma",
    "french": "Bonjour",
    "category": "salutations"
  }
]
```

---

### POST `/api/niveau2/audio`
Génère l'audio TTS d'un texte avec ElevenLabs.

**Request Body:**
```json
{
  "text": "I ni sogoma",
  "language": "fr"
}
```

**Response:**
- `Content-Type: audio/mpeg`
- Binary audio data (MP3)

**Usage Frontend:**
```javascript
const response = await fetch('/api/niveau2/audio', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({text: 'I ni sogoma', language: 'fr'})
});
const audioBlob = await response.blob();
const audioUrl = URL.createObjectURL(audioBlob);
const audio = new Audio(audioUrl);
audio.play();
```

---

## 🎤 NIVEAU 3 — Interaction Vocale + IA

### POST `/api/niveau3/text-chat`
Chat textuel avec l'IA Mistral (sans STT/TTS).

**Request Body:**
```json
{
  "text": "Je veux apprendre le Dioula",
  "expected_phrase": ""
}
```

**Response:**
```json
{
  "user_input": "Je veux apprendre le Dioula",
  "ai_response": "🗣️ En Dioula : N be dioula kalan k'a fe...",
  "similar_phrases": [...],
  "response_audio_base64": null
}
```

**Usage:**
- Conversation pédagogique en texte
- Mode démo sans micro
- Apprentissage guidé

---

### POST `/api/niveau3/voice-interaction`
**🎤 WOW EFFECT** - Pipeline complet STT → RAG → TTS

**Request:**
- `audio`: Fichier audio (WAV/MP3/WebM)
- `Content-Type: multipart/form-data`

**Response:**
```json
{
  "transcription": "I ni sogoma",
  "ai_response": "🗣️ En Dioula : I ni sogoma!...",
  "similar_phrases": [...],
  "response_audio_base64": "UklGRiQAAABXQVZF...",
  "score": 8
}
```

**Pipeline:**
1. **Whisper STT** : Transcrit l'audio
2. **Mistral RAG** : Génère réponse pédagogique
3. **ChromaDB** : Trouve phrases similaires
4. **ElevenLabs TTS** : Synthétise la réponse

**Usage Frontend:**
```javascript
const audioBlob = await recordAudio(); // WebRTC
const formData = new FormData();
formData.append('audio', audioBlob, 'recording.webm');

const response = await fetch('/api/niveau3/voice-interaction', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log('Transcription:', data.transcription);
console.log('AI:', data.ai_response);

// Play response audio
if (data.response_audio_base64) {
  const audioBytes = atob(data.response_audio_base64);
  // Convert to blob and play
}
```

---

### POST `/api/niveau3/evaluate-pronunciation`
Évalue la prononciation d'une phrase Dioula.

**Request:**
- `audio`: Fichier audio
- `expected`: Phrase attendue (query param ou form field)

**Response:**
```json
{
  "transcription": "i ni sogoma",
  "expected": "I ni sogoma",
  "score": 9,
  "score_max": 10,
  "feedback": "Très bonne prononciation!",
  "correct": true,
  "encouragement": "Parfait! I ni baara! 🎉"
}
```

---

## 🏥 HEALTH CHECK

### GET `/health`
Vérifie l'état du serveur.

**Response:**
```json
{
  "status": "ok",
  "rag_initialized": true,
  "llm_engine": "mistral-small",
  "mode": "full_rag"
}
```

---

## 🎯 Guide Frontend

### Flow Niveau 1
```
1. GET /api/niveau1/lessons → Afficher menu leçons
2. GET /api/niveau1/lessons/{id} → Afficher contenu
3. POST /api/niveau1/ask → Chatbot IA pour explications
4. GET /api/niveau1/lessons/{id}/quiz → Quiz
5. POST /api/niveau1/quiz/check → Validation
```

### Flow Niveau 2
```
1. GET /api/niveau2/phrases → Liste phrases audio
2. POST /api/niveau2/audio → Générer/jouer audio
3. Répétition vocale utilisateur (optionnel)
```

### Flow Niveau 3
```
1. Enregistrer audio utilisateur (WebRTC)
2. POST /api/niveau3/voice-interaction
   → STT + RAG + TTS automatique
3. Jouer réponse audio
4. Afficher transcription + feedback
```

---

## 🔧 Configuration CORS

Le serveur accepte les requêtes de **toutes origines** :
```python
origins = ["*"]
```

Pour production, limiter à :
```python
origins = ["https://votre-app.com"]
```

---

## 📊 Limites & Rate Limits

- **Mistral AI** : 500 requêtes/jour (gratuit)
- **ElevenLabs** : 10,000 caractères/mois (gratuit)
- **Whisper** : Local, pas de limite
- **ChromaDB** : 500 phrases indexées

---

## 🚀 Test Rapide

```bash
# Health check
curl http://127.0.0.1:8001/health

# Get lessons
curl http://127.0.0.1:8001/api/niveau1/lessons

# Ask AI
curl -X POST http://127.0.0.1:8001/api/niveau1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Comment dire bonjour?"}'

# Text chat
curl -X POST http://127.0.0.1:8001/api/niveau3/text-chat \
  -H "Content-Type: application/json" \
  -d '{"text": "Je veux apprendre le Dioula"}'
```

---

## 📖 Documentation Interactive

Accédez à la doc Swagger :
```
http://127.0.0.1:8001/docs
```

OpenAPI JSON :
```
http://127.0.0.1:8001/openapi.json
```

---

**🎉 Prêt pour le hackathon ! Bonne chance ! 🇨🇮**
