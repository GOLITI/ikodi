# 🎓 Microservice Apprentissage Dioula

Système d'apprentissage de la langue **Dioula (Dyula)** — Culture Ivoirienne 🇨🇮

## Stack Technique
- **FastAPI** — Backend REST
- **LangChain + ChromaDB** — RAG (Retrieval-Augmented Generation)
- **Whisper (OpenAI)** — Speech-to-Text local
- **ElevenLabs** — Text-to-Speech
- **Dataset**: [Koumankan4Dyula](https://huggingface.co/datasets/uvci/Koumankan_mt_dyu_fr) (10 929 paires Dioula-Français)

---

## 🚀 Installation rapide

```bash
# 1. Cloner et aller dans le dossier
cd dioula-microservice

# 2. Installer les dépendances Python
pip install -r requirements.txt

# 3. Configurer les clés API
cp .env.example .env
# → Remplir OPENAI_API_KEY, ELEVENLABS_API_KEY, HF_TOKEN dans .env

# 4. Lancer le serveur
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## 📖 Documentation API
Ouvrir: http://localhost:8001/docs

---

## 📚 Endpoints principaux

### Niveau 1 — Texte + Quiz
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/niveau1/lessons` | Liste des leçons |
| GET | `/api/niveau1/lessons/{id}` | Détail d'une leçon |
| GET | `/api/niveau1/lessons/{id}/quiz` | Questions du quiz |
| POST | `/api/niveau1/lessons/{id}/quiz/check` | Vérifier une réponse |

### Niveau 2 — Audio TTS
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/niveau2/audio?text=I+ni+ce` | Audio d'une phrase |
| GET | `/api/niveau2/lesson-audio/{lesson_id}/{index}` | Audio d'une phrase de leçon |

### Niveau 3 — IA Vocale (WOW)
| Méthode | Route | Description |
|---------|-------|-------------|
| POST | `/api/niveau3/voice-interaction` | Audio → Transcription → IA → Audio |
| POST | `/api/niveau3/text-chat` | Chat textuel avec l'IA |
| POST | `/api/niveau3/evaluate-pronunciation` | Score de prononciation |

---

## 🔑 Clés API requises

| Service | Lien | Plan gratuit |
|---------|------|-------------|
| OpenAI | https://platform.openai.com | Crédits de départ |
| ElevenLabs | https://elevenlabs.io | 10k chars/mois |
| HuggingFace | https://huggingface.co/settings/tokens | ✅ Gratuit |

---

## 💡 Mode sans clés API (Hackathon)
- **Niveau 1**: Fonctionne sans aucune clé (données statiques)
- **Niveau 2**: Nécessite ElevenLabs (ou utiliser des MP3 dans `audio_samples/`)
- **Niveau 3**: Nécessite OpenAI + ElevenLabs (fallback texte disponible)
