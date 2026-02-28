# 🎓 Guide Complet – Microservice 1 : Apprentissage Dioula
## Stack : FastAPI + LangChain + RAG + Whisper + ElevenLabs

---

## 📁 Structure du Projet

```
dioula-microservice/
├── app/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── config.py            # Variables d'environnement
│   ├── routers/
│   │   ├── niveau1.py       # Routes Niveau 1 (Texte + Quiz)
│   │   ├── niveau2.py       # Routes Niveau 2 (Texte + Audio)
│   │   └── niveau3.py       # Routes Niveau 3 (Interaction vocale IA)
│   ├── services/
│   │   ├── rag_service.py   # LangChain + RAG
│   │   ├── tts_service.py   # ElevenLabs TTS
│   │   └── stt_service.py   # Whisper STT
│   └── data/
│       ├── loader.py        # Chargement dataset HuggingFace
│       └── quiz_data.py     # Questions de quiz statiques
├── audio_samples/           # Fichiers audio pré-enregistrés
├── .env                     # Clés API
├── requirements.txt
└── README.md
```

---

## 🔧 ÉTAPE 1 – Installation & Configuration

### requirements.txt
```txt
fastapi==0.111.0
uvicorn[standard]==0.29.0
python-dotenv==1.0.1
langchain==0.2.0
langchain-community==0.2.0
langchain-openai==0.1.7
openai==1.30.0
chromadb==0.5.0
sentence-transformers==2.7.0
datasets==2.19.0
huggingface-hub==0.23.0
openai-whisper==20231117
elevenlabs==1.2.0
python-multipart==0.0.9
httpx==0.27.0
pydantic==2.7.0
```

### .env
```env
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
HF_TOKEN=hf_...
ELEVENLABS_VOICE_ID=your_voice_id
```

---

## 🚀 ÉTAPE 2 – Chargement du Dataset (data/loader.py)

```python
# app/data/loader.py
import os
from datasets import load_dataset
from typing import List, Dict

def load_dioula_pairs(max_samples: int = 500) -> List[Dict]:
    """
    Charge les paires dioula-français depuis HuggingFace.
    Dataset: uvci/Koumankan_mt_dyu_fr
    """
    try:
        dataset = load_dataset(
            "uvci/Koumankan_mt_dyu_fr",
            token=os.getenv("HF_TOKEN"),
            split="train"
        )
        
        pairs = []
        for i, row in enumerate(dataset):
            if i >= max_samples:
                break
            pairs.append({
                "dioula": row.get("sentence_dyu", ""),
                "french": row.get("sentence_fr", ""),
                "id": i
            })
        
        return pairs
    
    except Exception as e:
        print(f"Erreur chargement dataset: {e}")
        # Fallback avec données basiques si dataset indisponible
        return get_fallback_data()


def get_fallback_data() -> List[Dict]:
    """Données de base si le dataset est inaccessible"""
    return [
        {"dioula": "I ni ce", "french": "Bonjour / Salut", "id": 0},
        {"dioula": "I ni sogoma", "french": "Bonjour (matin)", "id": 1},
        {"dioula": "I ni wula", "french": "Bonsoir", "id": 2},
        {"dioula": "Aw ni ce", "french": "Bonjour (pluriel)", "id": 3},
        {"dioula": "Fo!", "french": "Salut!", "id": 4},
        {"dioula": "N togo ye...", "french": "Je m'appelle...", "id": 5},
        {"dioula": "I togo ye di?", "french": "Comment tu t'appelles?", "id": 6},
        {"dioula": "N be di", "french": "Je vais bien", "id": 7},
        {"dioula": "I be di wa?", "french": "Comment tu vas?", "id": 8},
        {"dioula": "N baro", "french": "Mon ami", "id": 9},
        {"dioula": "I kana balo", "french": "Ne t'inquiète pas", "id": 10},
        {"dioula": "Hali n'a tɛ", "french": "Même si ce n'est pas", "id": 11},
        {"dioula": "A ye di", "french": "C'est bon / C'est bien", "id": 12},
        {"dioula": "Nba", "french": "Mère", "id": 13},
        {"dioula": "Fa", "french": "Père", "id": 14},
        {"dioula": "Dɔgɔ", "french": "Petit frère / Petite sœur", "id": 15},
        {"dioula": "Kɔrɔ", "french": "Grand frère / Grande sœur", "id": 16},
        {"dioula": "Jɔ!", "french": "Arrête!", "id": 17},
        {"dioula": "Taa!", "french": "Va-t'en / Pars!", "id": 18},
        {"dioula": "Na!", "french": "Viens!", "id": 19},
    ]
```

---

## 🧠 ÉTAPE 3 – Service RAG avec LangChain (services/rag_service.py)

```python
# app/services/rag_service.py
import os
from typing import List, Dict, Optional
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.data.loader import load_dioula_pairs

# Prompt système pour l'IA Dioula
DIOULA_SYSTEM_PROMPT = """Tu es Souleymane, un professeur expert en langue Dioula (Dyula) 
de Côte d'Ivoire. Tu aides les apprenants à pratiquer le Dioula.

Contexte du corpus Dioula disponible:
{context}

Règles:
1. Réponds TOUJOURS en incluant la phrase en Dioula ET sa traduction française
2. Si l'utilisateur essaie de parler Dioula, évalue sa prononciation/orthographe
3. Encourage toujours l'apprenant avec bienveillance
4. Si la question concerne une phrase Dioula, donne des exemples similaires du corpus
5. Format de réponse: 
   - 🗣️ En Dioula: [phrase]
   - 🇫🇷 En Français: [traduction]
   - 💡 Conseil: [conseil pédagogique]

Question de l'apprenant: {question}"""

class DioulaRAGService:
    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self.qa_chain = None
        self._initialized = False
    
    def initialize(self):
        """Initialise le RAG avec le dataset Dioula"""
        if self._initialized:
            return
        
        print("🔄 Initialisation du RAG Dioula...")
        
        # Charger les données
        pairs = load_dioula_pairs(max_samples=500)
        
        # Créer les documents LangChain
        documents = []
        for pair in pairs:
            content = f"Dioula: {pair['dioula']}\nFrançais: {pair['french']}"
            doc = Document(
                page_content=content,
                metadata={"id": pair["id"], "dioula": pair["dioula"], "french": pair["french"]}
            )
            documents.append(doc)
        
        # Embeddings et VectorStore
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name="dioula_corpus"
        )
        
        # LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            max_tokens=500
        )
        
        # Prompt
        prompt = PromptTemplate(
            template=DIOULA_SYSTEM_PROMPT,
            input_variables=["context", "question"]
        )
        
        # Chaîne QA
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": prompt}
        )
        
        self._initialized = True
        print("✅ RAG Dioula initialisé!")
    
    def query(self, question: str) -> str:
        """Pose une question au RAG"""
        if not self._initialized:
            self.initialize()
        
        result = self.qa_chain.invoke({"query": question})
        return result["result"]
    
    def search_similar(self, text: str, k: int = 3) -> List[Dict]:
        """Cherche des phrases similaires dans le corpus"""
        if not self._initialized:
            self.initialize()
        
        docs = self.vectorstore.similarity_search(text, k=k)
        return [
            {"dioula": doc.metadata["dioula"], "french": doc.metadata["french"]}
            for doc in docs
        ]
    
    def evaluate_dioula(self, user_input: str, expected: str) -> Dict:
        """Évalue la réponse Dioula de l'utilisateur"""
        question = f"""L'apprenant a dit: "{user_input}"
        La réponse attendue était: "{expected}"
        
        Évalue sur 10, explique les erreurs, et donne la forme correcte."""
        
        feedback = self.query(question)
        
        # Score simple basé sur similarité de caractères
        from difflib import SequenceMatcher
        similarity = SequenceMatcher(None, 
            user_input.lower().strip(), 
            expected.lower().strip()
        ).ratio()
        score = round(similarity * 10, 1)
        
        return {
            "score": score,
            "feedback": feedback,
            "correct": similarity > 0.7
        }

# Instance globale
rag_service = DioulaRAGService()
```

---

## 🔊 ÉTAPE 4 – Service Text-to-Speech ElevenLabs (services/tts_service.py)

```python
# app/services/tts_service.py
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import hashlib
from pathlib import Path

AUDIO_CACHE_DIR = Path("audio_samples/cache")
AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)

class TTSService:
    def __init__(self):
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    
    def text_to_speech(self, text: str, language: str = "dioula") -> bytes:
        """Convertit du texte en audio avec ElevenLabs"""
        
        # Cache : évite de re-générer les mêmes audios
        cache_key = hashlib.md5(f"{text}_{language}".encode()).hexdigest()
        cache_file = AUDIO_CACHE_DIR / f"{cache_key}.mp3"
        
        if cache_file.exists():
            return cache_file.read_bytes()
        
        # Génération audio
        audio = self.client.generate(
            text=text,
            voice=self.voice_id,
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=True
            ),
            model="eleven_multilingual_v2"  # Supporte les langues africaines
        )
        
        # Convertir le générateur en bytes
        audio_bytes = b"".join(audio)
        
        # Sauvegarder en cache
        cache_file.write_bytes(audio_bytes)
        
        return audio_bytes
    
    def generate_lesson_audio(self, dioula: str, french: str) -> bytes:
        """Génère audio pour une leçon (Dioula + traduction)"""
        combined_text = f"{dioula}. En français: {french}"
        return self.text_to_speech(combined_text)


tts_service = TTSService()
```

---

## 🎤 ÉTAPE 5 – Service Speech-to-Text Whisper (services/stt_service.py)

```python
# app/services/stt_service.py
import whisper
import tempfile
import os
from pathlib import Path

class WhisperSTTService:
    def __init__(self):
        # "base" = rapide, "small" = meilleur pour langues africaines
        print("🔄 Chargement du modèle Whisper...")
        self.model = whisper.load_model("base")
        print("✅ Whisper chargé!")
    
    def transcribe(self, audio_bytes: bytes, language: str = None) -> dict:
        """
        Transcrit un audio en texte.
        Pour le Dioula, on laisse Whisper détecter automatiquement
        ou on force le français comme langue proche.
        """
        
        # Écrire l'audio dans un fichier temporaire
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        
        try:
            # Transcrire
            # Note: Whisper ne supporte pas natif le Dioula,
            # mais "fr" donne de meilleurs résultats pour les langues
            # d'Afrique de l'Ouest avec alphabet latin
            options = {
                "task": "transcribe",
                "language": language or "fr",  # fr comme approximation
                "fp16": False
            }
            
            result = self.model.transcribe(tmp_path, **options)
            
            return {
                "text": result["text"].strip(),
                "language": result.get("language", "unknown"),
                "segments": result.get("segments", [])
            }
        
        finally:
            os.unlink(tmp_path)
    
    def transcribe_dioula(self, audio_bytes: bytes) -> str:
        """Transcription optimisée pour le Dioula"""
        result = self.transcribe(audio_bytes, language=None)  # Auto-detect
        return result["text"]


stt_service = WhisperSTTService()
```

---

## 📚 ÉTAPE 6 – Quiz Data (data/quiz_data.py)

```python
# app/data/quiz_data.py
# Questions de quiz pour Niveau 1 et Niveau 2

NIVEAU1_LESSONS = [
    {
        "id": 1,
        "title": "Les Salutations",
        "theme": "greetings",
        "content": [
            {"dioula": "I ni ce", "french": "Bonjour / Salut", "context": "Salutation générale"},
            {"dioula": "I ni sogoma", "french": "Bonjour (matin)", "context": "Le matin"},
            {"dioula": "I ni wula", "french": "Bonsoir", "context": "Le soir"},
            {"dioula": "I be di wa?", "french": "Comment tu vas?", "context": "Demander des nouvelles"},
            {"dioula": "N be di", "french": "Je vais bien", "context": "Répondre positivement"},
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "Comment dit-on 'Bonjour' en Dioula ?",
                "options": ["I ni ce", "N be di", "Taa!", "Fo!"],
                "correct": 0,
                "explanation": "I ni ce est la salutation la plus courante en Dioula"
            },
            {
                "id": "q2",
                "question": "Que signifie 'I be di wa?' ?",
                "options": [
                    "Je m'appelle...",
                    "Au revoir",
                    "Comment tu vas?",
                    "Merci beaucoup"
                ],
                "correct": 2,
                "explanation": "I be di wa? est la façon de demander 'comment vas-tu?' en Dioula"
            },
            {
                "id": "q3",
                "question": "Comment répondre positivement à 'I be di wa?' ?",
                "options": ["Taa!", "N be di", "I ni wula", "Jɔ!"],
                "correct": 1,
                "explanation": "N be di signifie 'je vais bien'"
            }
        ]
    },
    {
        "id": 2,
        "title": "La Famille",
        "theme": "family",
        "content": [
            {"dioula": "Nba", "french": "Mère", "context": "Membre de la famille"},
            {"dioula": "Fa", "french": "Père", "context": "Membre de la famille"},
            {"dioula": "Dɔgɔ", "french": "Petit frère / Petite sœur", "context": "Fratrie"},
            {"dioula": "Kɔrɔ", "french": "Grand frère / Grande sœur", "context": "Fratrie"},
            {"dioula": "Den", "french": "Enfant", "context": "Famille"},
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "Comment dit-on 'Mère' en Dioula ?",
                "options": ["Fa", "Nba", "Den", "Kɔrɔ"],
                "correct": 1,
                "explanation": "Nba désigne la mère en Dioula"
            },
            {
                "id": "q2",
                "question": "Que signifie 'Dɔgɔ' ?",
                "options": ["Grand frère", "Père", "Petit frère/sœur", "Enfant"],
                "correct": 2,
                "explanation": "Dɔgɔ désigne le petit frère ou la petite sœur"
            }
        ]
    },
    {
        "id": 3,
        "title": "Présentations",
        "theme": "introductions",
        "content": [
            {"dioula": "N togo ye...", "french": "Je m'appelle...", "context": "Se présenter"},
            {"dioula": "I togo ye di?", "french": "Comment tu t'appelles?", "context": "Demander le prénom"},
            {"dioula": "N baro", "french": "Mon ami", "context": "Amitié"},
            {"dioula": "N ye ivoirien ye", "french": "Je suis ivoirien", "context": "Nationalité"},
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "Comment demande-t-on le prénom de quelqu'un ?",
                "options": ["N togo ye", "I togo ye di?", "N be di", "Fo!"],
                "correct": 1,
                "explanation": "I togo ye di? signifie 'Comment tu t'appelles?'"
            }
        ]
    }
]

NIVEAU2_LESSONS = [
    {
        "id": 1,
        "title": "Sons et Tonalités",
        "theme": "pronunciation",
        "content": [
            {
                "dioula": "A ye baara kɛ",
                "french": "Il/Elle a travaillé",
                "audio_key": "a_ye_baara",
                "phonetic": "a yé ba-ra ké",
                "note": "Notez la tonalité descendante sur 'kɛ'"
            },
            {
                "dioula": "Ne bɛ taa sugu la",
                "french": "Je vais au marché",
                "audio_key": "taa_sugu",
                "phonetic": "né bè ta su-gou la",
                "note": "Phrase du quotidien très utilisée"
            },
            {
                "dioula": "Dugu kɔnɔ",
                "french": "Dans le village",
                "audio_key": "dugu_kono",
                "phonetic": "dou-gou kɔ-nɔ",
                "note": "Le 'ɔ' est une voyelle ouverte"
            },
        ]
    }
]
```

---

## 🌐 ÉTAPE 7 – Routes API (routers/)

### routers/niveau1.py
```python
# app/routers/niveau1.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.data.quiz_data import NIVEAU1_LESSONS

router = APIRouter(prefix="/api/niveau1", tags=["Niveau 1"])

class QuizAnswer(BaseModel):
    lesson_id: int
    question_id: str
    answer_index: int

@router.get("/lessons")
async def get_all_lessons():
    """Récupère toutes les leçons Niveau 1"""
    return {
        "lessons": [
            {"id": l["id"], "title": l["title"], "theme": l["theme"]}
            for l in NIVEAU1_LESSONS
        ]
    }

@router.get("/lessons/{lesson_id}")
async def get_lesson(lesson_id: int):
    """Récupère une leçon complète avec contenu"""
    lesson = next((l for l in NIVEAU1_LESSONS if l["id"] == lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Leçon non trouvée")
    return lesson

@router.get("/lessons/{lesson_id}/quiz")
async def get_quiz(lesson_id: int):
    """Récupère les questions de quiz d'une leçon"""
    lesson = next((l for l in NIVEAU1_LESSONS if l["id"] == lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Leçon non trouvée")
    
    # Retourner quiz sans les bonnes réponses
    quiz_public = []
    for q in lesson["quiz"]:
        quiz_public.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        })
    return {"quiz": quiz_public}

@router.post("/lessons/{lesson_id}/quiz/check")
async def check_answer(lesson_id: int, answer: QuizAnswer):
    """Vérifie une réponse de quiz"""
    lesson = next((l for l in NIVEAU1_LESSONS if l["id"] == lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Leçon non trouvée")
    
    question = next((q for q in lesson["quiz"] if q["id"] == answer.question_id), None)
    if not question:
        raise HTTPException(status_code=404, detail="Question non trouvée")
    
    is_correct = answer.answer_index == question["correct"]
    
    return {
        "correct": is_correct,
        "correct_index": question["correct"],
        "explanation": question["explanation"],
        "score_points": 10 if is_correct else 0
    }
```

### routers/niveau2.py
```python
# app/routers/niveau2.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.services.tts_service import tts_service
from app.data.quiz_data import NIVEAU2_LESSONS, NIVEAU1_LESSONS

router = APIRouter(prefix="/api/niveau2", tags=["Niveau 2"])

@router.get("/lessons")
async def get_lessons():
    """Leçons Niveau 2 avec support audio"""
    return {"lessons": NIVEAU2_LESSONS}

@router.get("/audio/{dioula_text}")
async def get_audio(dioula_text: str):
    """
    Génère ou récupère l'audio d'une phrase Dioula.
    Utilise ElevenLabs pour la synthèse vocale.
    """
    try:
        audio_bytes = tts_service.text_to_speech(dioula_text)
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=dioula.mp3"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur TTS: {str(e)}")

@router.get("/lesson-audio/{lesson_id}/{phrase_index}")
async def get_lesson_phrase_audio(lesson_id: int, phrase_index: int):
    """Audio pour une phrase spécifique d'une leçon"""
    # Cherche dans les deux niveaux
    all_lessons = NIVEAU1_LESSONS + NIVEAU2_LESSONS
    lesson = next((l for l in all_lessons if l["id"] == lesson_id), None)
    
    if not lesson or phrase_index >= len(lesson["content"]):
        raise HTTPException(status_code=404, detail="Phrase non trouvée")
    
    phrase = lesson["content"][phrase_index]
    
    try:
        audio_bytes = tts_service.generate_lesson_audio(
            phrase["dioula"], 
            phrase["french"]
        )
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### routers/niveau3.py
```python
# app/routers/niveau3.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from app.services.stt_service import stt_service
from app.services.tts_service import tts_service
from app.services.rag_service import rag_service
from fastapi.responses import Response

router = APIRouter(prefix="/api/niveau3", tags=["Niveau 3 - WOW"])

class TextInteraction(BaseModel):
    text: str
    expected_phrase: str = ""

@router.post("/voice-interaction")
async def voice_interaction(audio: UploadFile = File(...)):
    """
    🎤 INTERACTION VOCALE COMPLÈTE:
    1. Reçoit l'audio de l'utilisateur
    2. Transcrit avec Whisper
    3. Répond avec l'IA (RAG Dioula)
    4. Génère l'audio de réponse avec ElevenLabs
    """
    
    # 1. Lire l'audio
    audio_bytes = await audio.read()
    
    # 2. Speech-to-Text avec Whisper
    try:
        transcription = stt_service.transcribe_dioula(audio_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur STT: {str(e)}")
    
    # 3. Réponse IA avec RAG
    try:
        ai_response = rag_service.query(
            f"L'apprenant a dit en Dioula ou essaie de parler Dioula: '{transcription}'. "
            f"Réponds en Dioula avec la traduction française."
        )
    except Exception as e:
        ai_response = "N be i fɛ. Tu fais des progrès!"  # Fallback
    
    # 4. Chercher des phrases similaires
    similar = rag_service.search_similar(transcription, k=2)
    
    # 5. Générer l'audio de réponse
    try:
        response_audio = tts_service.text_to_speech(ai_response)
        audio_base64 = __import__('base64').b64encode(response_audio).decode()
    except Exception:
        audio_base64 = None
    
    return {
        "transcription": transcription,
        "ai_response": ai_response,
        "similar_phrases": similar,
        "response_audio_base64": audio_base64,
        "score": _compute_simple_score(transcription)
    }

@router.post("/evaluate-pronunciation")
async def evaluate_pronunciation(
    audio: UploadFile = File(...),
    expected: str = ""
):
    """Évalue la prononciation de l'utilisateur"""
    audio_bytes = await audio.read()
    
    transcription = stt_service.transcribe_dioula(audio_bytes)
    evaluation = rag_service.evaluate_dioula(transcription, expected)
    
    return {
        "transcription": transcription,
        "expected": expected,
        "score": evaluation["score"],
        "feedback": evaluation["feedback"],
        "correct": evaluation["correct"]
    }

@router.post("/text-chat")
async def text_chat(interaction: TextInteraction):
    """Chat textuel avec l'IA Dioula (sans audio, pour démo rapide)"""
    response = rag_service.query(interaction.text)
    
    return {
        "user_input": interaction.text,
        "ai_response": response,
        "similar_phrases": rag_service.search_similar(interaction.text, k=3)
    }

def _compute_simple_score(transcription: str) -> int:
    """Score simple basé sur la longueur et présence de mots Dioula"""
    dioula_keywords = ["ni", "ce", "be", "ye", "taa", "na", "di", "wa", "fo", "ba"]
    words = transcription.lower().split()
    matches = sum(1 for w in words if w in dioula_keywords)
    
    if len(words) == 0:
        return 0
    
    score = min(100, (matches / max(len(words), 1)) * 100 + len(words) * 5)
    return int(score)
```

---

## 🏠 ÉTAPE 8 – Application Principale (main.py)

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import niveau1, niveau2, niveau3
from app.services.rag_service import rag_service
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise les services au démarrage"""
    print("🚀 Démarrage du Microservice Dioula...")
    
    # Initialiser le RAG en arrière-plan
    try:
        rag_service.initialize()
        print("✅ RAG Service initialisé")
    except Exception as e:
        print(f"⚠️ RAG non initialisé (mode dégradé): {e}")
    
    yield
    print("🛑 Arrêt du microservice")


app = FastAPI(
    title="🎓 Microservice Apprentissage Dioula",
    description="""
    API pour l'apprentissage de la langue Dioula (Dyula) - Culture Ivoirienne
    
    ## Niveaux
    - **Niveau 1**: Texte + Quiz interactif
    - **Niveau 2**: Texte + Audio (ElevenLabs TTS)  
    - **Niveau 3**: Interaction vocale IA (Whisper + RAG + ElevenLabs)
    
    ## Dataset
    Basé sur le corpus Koumankan4Dyula (10,929 paires Dioula-Français)
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS pour React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(niveau1.router)
app.include_router(niveau2.router)
app.include_router(niveau3.router)

@app.get("/")
async def root():
    return {
        "service": "Microservice Apprentissage Dioula",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "niveau1": "/api/niveau1/lessons",
            "niveau2": "/api/niveau2/lessons",
            "niveau3": "/api/niveau3/voice-interaction",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok", "rag_ready": rag_service._initialized}
```

---

## 🏃 ÉTAPE 9 – Lancement

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer l'environnement
cp .env.example .env
# Remplir les clés API dans .env

# 3. Lancer le serveur
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# 4. Tester l'API
# → http://localhost:8001/docs  (Swagger UI automatique)
```

---

## 🧪 ÉTAPE 10 – Tests Rapides

```bash
# Test Niveau 1 - Récupérer les leçons
curl http://localhost:8001/api/niveau1/lessons

# Test Niveau 1 - Vérifier une réponse quiz
curl -X POST http://localhost:8001/api/niveau1/lessons/1/quiz/check \
  -H "Content-Type: application/json" \
  -d '{"lesson_id": 1, "question_id": "q1", "answer_index": 0}'

# Test Niveau 2 - Obtenir un audio
curl http://localhost:8001/api/niveau2/audio/I%20ni%20ce --output salutation.mp3

# Test Niveau 3 - Chat textuel (plus simple à tester)
curl -X POST http://localhost:8001/api/niveau3/text-chat \
  -H "Content-Type: application/json" \
  -d '{"text": "Comment dire bonjour en Dioula?", "expected_phrase": ""}'
```

---

## 🔑 Clés API nécessaires

| Service | Où l'obtenir | Gratuit? |
|---------|-------------|----------|
| OpenAI API | platform.openai.com | Non (~$5 crédit de départ) |
| ElevenLabs | elevenlabs.io | Oui (10k chars/mois) |
| HuggingFace | huggingface.co/settings/tokens | Oui |

---

## 💡 Astuce Hackathon – Mode Sans Clés API

Si vous n'avez pas les clés, activez le mode fallback dans `config.py`:
- Niveau 1: Fonctionne 100% sans API (données statiques)
- Niveau 2: Utiliser des fichiers MP3 pré-générés dans `/audio_samples/`  
- Niveau 3: Réponses pré-scriptées si OpenAI indisponible

---

## 📊 Architecture Résumée

```
React Frontend (port 3000)
        ↓ HTTP
FastAPI Backend (port 8001)
    ├── /api/niveau1/* → Quiz statiques (pas d'API externe)
    ├── /api/niveau2/* → ElevenLabs TTS → Audio MP3
    └── /api/niveau3/*
            ├── Whisper (local) → Transcription
            ├── LangChain RAG + ChromaDB → Réponse IA
            └── ElevenLabs → Audio réponse
                    ↑
            Dataset HuggingFace
            (Koumankan4Dyula)
```
