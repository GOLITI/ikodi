from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.services.tts_service import tts_service
from app.data.quiz_data import NIVEAU1_LESSONS, NIVEAU2_AUDIO_PHRASES
import urllib.parse

router = APIRouter(prefix="/api/niveau2", tags=["Niveau 2 – Audio"])


@router.get("/phrases")
async def get_audio_phrases():
    """Liste des phrases disponibles avec audio"""
    return {"phrases": NIVEAU2_AUDIO_PHRASES}


@router.get("/audio")
async def get_audio_for_text(text: str):
    """
    Génère ou récupère l'audio d'une phrase Dioula.
    Exemple: GET /api/niveau2/audio?text=I%20ni%20ce
    """
    if not text or len(text) > 5000:
        raise HTTPException(status_code=400, detail="Texte trop long (max 5000 caractères)")

    try:
        audio_bytes = tts_service.text_to_speech(text)
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"inline; filename=dioula.mp3"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur génération audio: {str(e)}")


@router.get("/lesson-audio/{lesson_id}/{phrase_index}")
async def get_lesson_phrase_audio(lesson_id: int, phrase_index: int):
    """Audio pour une phrase spécifique d'une leçon (Dioula + traduction FR)"""
    lesson = next((l for l in NIVEAU1_LESSONS if l["id"] == lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Leçon non trouvée")
    if phrase_index >= len(lesson["content"]):
        raise HTTPException(status_code=404, detail="Index de phrase hors limites")

    phrase = lesson["content"][phrase_index]

    try:
        audio_bytes = tts_service.generate_lesson_audio(
            phrase["dioula"],
            phrase["french"]
        )
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/phrase-audio/{phrase_id}")
async def get_phrase_audio(phrase_id: int):
    """Audio pour une phrase du catalogue Niveau 2"""
    phrase = next((p for p in NIVEAU2_AUDIO_PHRASES if p["id"] == phrase_id), None)
    if not phrase:
        raise HTTPException(status_code=404, detail="Phrase non trouvée")

    try:
        audio_bytes = tts_service.generate_lesson_audio(phrase["dioula"], phrase["french"])
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
