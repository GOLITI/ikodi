import base64
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from app.services.stt_service import stt_service
from app.services.tts_service import tts_service
from app.services.rag_service import rag_service
from fastapi.responses import Response

router = APIRouter(prefix="/api/niveau3", tags=["Niveau 3 – WOW 🎤 IA Vocale"])


class TextChat(BaseModel):
    text: str
    expected_phrase: str = ""


@router.post("/voice-interaction")
async def voice_interaction(audio: UploadFile = File(...)):
    """
    🎤 INTERACTION VOCALE COMPLÈTE (WOW EFFECT):
    1. Reçoit l'audio de l'utilisateur (WAV/MP3/WebM)
    2. Transcrit avec Whisper (speech-to-text local)
    3. Cherche dans le corpus Dioula (RAG)
    4. Génère une réponse pédagogique (IA)
    5. Synthétise la réponse en audio (ElevenLabs)
    """
    print(f"[VOICE] Reception audio: {audio.filename}, type: {audio.content_type}")
    audio_bytes = await audio.read()
    print(f"[VOICE] Taille audio: {len(audio_bytes)} bytes")

    # Étape 1: Transcription Whisper
    try:
        print("[VOICE] Transcription Whisper...")
        transcription = stt_service.transcribe_dioula(audio_bytes)
        print(f"[VOICE] Transcription: '{transcription}'")
    except Exception as e:
        print(f"[VOICE ERROR] STT: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur STT Whisper: {str(e)}")

    if not transcription:
        raise HTTPException(status_code=400, detail="Audio non reconnu. Parlez plus clairement.")

    # Étape 2: Réponse IA avec RAG
    try:
        print("[VOICE] Generation reponse IA...")
        ai_response = rag_service.query(
            f"L'apprenant a dit ou essayé de dire en Dioula: '{transcription}'. "
            f"Réponds en Dioula avec la traduction française et encourage-le."
        )
        print(f"[VOICE] AI: '{ai_response[:100]}...'")
    except Exception as ex:
        print(f"[VOICE ERROR] RAG: {str(ex)}")
        ai_response = "I ni ce! N be i fɛ. Tu fais de bons progrès! 🌍"

    # Étape 3: Phrases similaires du corpus
    print("[VOICE] Recherche phrases similaires...")
    similar = rag_service.search_similar(transcription, k=3)
    print(f"[VOICE] {len(similar)} phrases trouvees")

    # Étape 4: Audio de la réponse IA
    audio_base64 = None
    try:
        print("[VOICE] Generation TTS...")
        response_audio = tts_service.text_to_speech(ai_response)
        audio_base64 = base64.b64encode(response_audio).decode("utf-8")
        print(f"[VOICE] TTS audio: {len(audio_base64)} chars base64")
    except Exception as ex:
        print(f"[VOICE ERROR] TTS: {str(ex)}")
        pass  # Audio optionnel

    print("[VOICE] Reponse complete!")
    return {
        "transcription": transcription,
        "ai_response": ai_response,
        "similar_phrases": similar,
        "response_audio_base64": audio_base64,
        "score": _compute_simple_score(transcription),
    }


@router.post("/evaluate-pronunciation")
async def evaluate_pronunciation(
    audio: UploadFile = File(...),
    expected: str = ""
):
    """
    Évalue la prononciation d'une phrase Dioula donnée.
    Retourne un score et des conseils.
    """
    audio_bytes = await audio.read()
    transcription = stt_service.transcribe_dioula(audio_bytes)
    evaluation = rag_service.evaluate_dioula(transcription, expected)

    return {
        "transcription": transcription,
        "expected": expected,
        "score": evaluation["score"],
        "score_max": 10,
        "feedback": evaluation["feedback"],
        "correct": evaluation["correct"],
        "encouragement": "Parfait! I ni baara! 🎉" if evaluation["correct"] else "Continue! I kana balo! 💪"
    }


@router.post("/text-chat")
async def text_chat(interaction: TextChat):
    """
    Chat textuel avec l'IA Dioula.
    Utile pour tester sans micro ou pour la démo.
    """
    response = rag_service.query(interaction.text)
    similar = rag_service.search_similar(interaction.text, k=3)

    # Audio optionnel de la réponse
    audio_base64 = None
    try:
        print("[TEXT-CHAT] Generation TTS...")
        audio_bytes = tts_service.text_to_speech(response)
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        print(f"[TEXT-CHAT] TTS OK: {len(audio_base64)} chars base64")
    except Exception as ex:
        print(f"[TEXT-CHAT ERROR] TTS: {str(ex)}")
        pass

    return {
        "user_input": interaction.text,
        "ai_response": response,
        "similar_phrases": similar,
        "response_audio_base64": audio_base64,
    }


def _compute_simple_score(transcription: str) -> int:
    """Score simple: présence de mots Dioula reconnus"""
    dioula_words = {
        "ni", "ce", "be", "ye", "taa", "na", "di", "wa", "fo", "ba",
        "nba", "fa", "togo", "baro", "sogoma", "wula", "sugu", "juru",
        "den", "ko", "la", "ne", "an", "aw", "bɛ", "kɛ", "sɔrɔ"
    }
    words = set(transcription.lower().split())
    matches = len(words & dioula_words)
    base_score = min(100, matches * 20 + len(transcription.split()) * 5)
    return int(base_score)
