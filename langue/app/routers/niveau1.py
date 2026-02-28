# app/routers/niveau1.py  —  VERSION GEMINI
# Niveau 1 : Texte + Quiz (statique) + Explications IA (Gemini)
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from app.data.quiz_data import NIVEAU1_LESSONS
from app.services.rag_service import rag_service

router = APIRouter(prefix="/api/niveau1", tags=["Niveau 1 — Texte & Quiz"])


# ── Modèles Pydantic ─────────────────────────────────────────

class QuizAnswer(BaseModel):
    lesson_id: int
    question_id: str
    answer_index: int

class QuizSession(BaseModel):
    """Score d'une session de quiz complète"""
    lesson_id: int
    answers: list[dict]  # [{"question_id": "q1", "answer_index": 0}, ...]

class AskQuestion(BaseModel):
    """Question libre posée à Souleymane (l'IA Gemini)"""
    question: str


# ── GET /api/niveau1/lessons ─────────────────────────────────

@router.get("/lessons", summary="Liste de toutes les leçons")
async def get_all_lessons():
    """Retourne la liste des leçons avec métadonnées (sans le contenu complet)"""
    return {
        "total": len(NIVEAU1_LESSONS),
        "lessons": [
            {
                "id":           l["id"],
                "title":        l["title"],
                "theme":        l["theme"],
                "emoji":        l.get("emoji", "📚"),
                "description":  l.get("description", ""),
                "phrase_count": len(l["content"]),
                "quiz_count":   len(l["quiz"]),
            }
            for l in NIVEAU1_LESSONS
        ],
    }


# ── GET /api/niveau1/lessons/{id} ────────────────────────────

@router.get("/lessons/{lesson_id}", summary="Contenu complet d'une leçon")
async def get_lesson(lesson_id: int):
    """Retourne toutes les phrases + quiz d'une leçon"""
    lesson = _find_lesson(lesson_id)
    return lesson


# ── GET /api/niveau1/lessons/{id}/quiz ───────────────────────

@router.get("/lessons/{lesson_id}/quiz", summary="Questions de quiz (sans les réponses)")
async def get_quiz(lesson_id: int):
    """Retourne les questions du quiz sans révéler les bonnes réponses"""
    lesson = _find_lesson(lesson_id)
    quiz_public = [
        {"id": q["id"], "question": q["question"], "options": q["options"]}
        for q in lesson["quiz"]
    ]
    return {
        "lesson_id": lesson_id,
        "lesson_title": lesson["title"],
        "quiz": quiz_public,
        "total": len(quiz_public),
    }


# ── POST /api/niveau1/lessons/{id}/quiz/check ────────────────

@router.post("/lessons/{lesson_id}/quiz/check", summary="Vérifier une réponse")
async def check_answer(lesson_id: int, answer: QuizAnswer):
    """
    Vérifie une réponse de quiz.
    Retourne : correct, bonne réponse, explication statique + encouragement Dioula.
    """
    lesson = _find_lesson(lesson_id)
    question = next((q for q in lesson["quiz"] if q["id"] == answer.question_id), None)
    if not question:
        raise HTTPException(status_code=404, detail="Question non trouvée")

    is_correct = answer.answer_index == question["correct"]

    return {
        "correct":        is_correct,
        "correct_index":  question["correct"],
        "correct_answer": question["options"][question["correct"]],
        "explanation":    question["explanation"],
        "score_points":   10 if is_correct else 0,
        "encouragement":  "I ni baara! Excellent! 🎉" if is_correct else "I kana balo! Essaie encore! 💪",
    }


# ── POST /api/niveau1/lessons/{id}/quiz/session ──────────────

@router.post("/lessons/{lesson_id}/quiz/session", summary="Soumettre toutes les réponses d'un quiz")
async def submit_quiz_session(lesson_id: int, session: QuizSession):
    """
    Soumet toutes les réponses d'une session de quiz en une fois.
    Retourne le score total, les corrections et un message Gemini personnalisé.
    """
    lesson = _find_lesson(lesson_id)
    results = []
    total_correct = 0

    for ans in session.answers:
        question = next((q for q in lesson["quiz"] if q["id"] == ans.get("question_id")), None)
        if not question:
            continue
        is_correct = ans.get("answer_index") == question["correct"]
        if is_correct:
            total_correct += 1
        results.append({
            "question_id":    question["id"],
            "question":       question["question"],
            "your_answer":    question["options"][ans.get("answer_index", 0)] if 0 <= ans.get("answer_index", -1) < len(question["options"]) else "—",
            "correct_answer": question["options"][question["correct"]],
            "correct":        is_correct,
            "explanation":    question["explanation"],
        })

    total_questions = len(results)
    percentage = round((total_correct / total_questions) * 100) if total_questions else 0

    # Message Gemini adapté au score
    if percentage == 100:
        gemini_message = rag_service.query(
            f"L'apprenant a eu 100% au quiz sur '{lesson['title']}'. "
            f"Félicite-le chaleureusement en Dioula et encourage-le à passer au niveau suivant."
        )
    elif percentage >= 60:
        gemini_message = rag_service.query(
            f"L'apprenant a eu {percentage}% au quiz sur '{lesson['title']}'. "
            f"Encourage-le avec un message motivant en Dioula."
        )
    else:
        gemini_message = rag_service.query(
            f"L'apprenant a eu {percentage}% au quiz sur '{lesson['title']}'. "
            f"Console-le avec bienveillance en Dioula et donne un conseil pour progresser."
        )

    return {
        "lesson_id":       lesson_id,
        "lesson_title":    lesson["title"],
        "score":           total_correct,
        "total":           total_questions,
        "percentage":      percentage,
        "passed":          percentage >= 60,
        "results":         results,
        "gemini_feedback": gemini_message,
        "badge":           _get_badge(percentage),
    }


# ── GET /api/niveau1/lessons/{id}/explain/{index} ────────────

@router.get(
    "/lessons/{lesson_id}/explain/{phrase_index}",
    summary="Explication IA d'une phrase (Gemini)"
)
async def explain_phrase(lesson_id: int, phrase_index: int):
    """
    Demande à Gemini d'expliquer en détail une phrase Dioula :
    contexte d'usage, variantes, exemples.
    """
    lesson = _find_lesson(lesson_id)
    if phrase_index >= len(lesson["content"]):
        raise HTTPException(status_code=404, detail="Index de phrase hors limites")

    phrase = lesson["content"][phrase_index]
    explanation = rag_service.explain_phrase(phrase["dioula"], phrase["french"])

    return {
        "phrase":      phrase,
        "explanation": explanation,
        "lesson":      lesson["title"],
    }


# ── POST /api/niveau1/ask ─────────────────────────────────────

@router.post("/ask", summary="Poser une question libre à Souleymane (IA Gemini)")
async def ask_souleymane(body: AskQuestion):
    """
    L'apprenant peut poser n'importe quelle question sur le Dioula.
    Gemini répond en s'appuyant sur le corpus Koumankan (RAG).
    """
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="La question ne peut pas être vide")

    response = rag_service.query(body.question)
    similar  = rag_service.search_similar(body.question, k=3)

    return {
        "question":       body.question,
        "answer":         response,
        "similar_phrases": similar,
    }


# ── GET /api/niveau1/lessons/{id}/quiz/dynamic ───────────────

@router.get(
    "/lessons/{lesson_id}/quiz/dynamic",
    summary="Générer une question de quiz avec Gemini"
)
async def get_dynamic_quiz_question(lesson_id: int):
    """
    Génère une nouvelle question de quiz dynamique avec Gemini.
    Différente à chaque appel — utile pour enrichir la banque de questions.
    """
    lesson = _find_lesson(lesson_id)
    generated = rag_service.generate_quiz_question(lesson["content"])

    if not generated:
        raise HTTPException(
            status_code=503,
            detail="Génération de question non disponible (Gemini requis)"
        )

    return {
        "lesson_id":    lesson_id,
        "lesson_title": lesson["title"],
        "question":     generated,
        "source":       "gemini_generated",
    }


# ── GET /api/niveau1/search ───────────────────────────────────

@router.get("/search", summary="Chercher des phrases Dioula similaires")
async def search_dioula(q: str, k: int = 5):
    """
    Recherche sémantique dans le corpus Dioula.
    Exemple: GET /api/niveau1/search?q=bonjour&k=5
    """
    if not q.strip():
        raise HTTPException(status_code=400, detail="Paramètre q manquant")

    results = rag_service.search_similar(q, k=min(k, 10))
    return {
        "query":   q,
        "results": results,
        "count":   len(results),
    }


# ── Helpers privés ────────────────────────────────────────────

def _find_lesson(lesson_id: int) -> dict:
    lesson = next((l for l in NIVEAU1_LESSONS if l["id"] == lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail=f"Leçon {lesson_id} non trouvée")
    return lesson


def _get_badge(percentage: int) -> dict:
    if percentage == 100:
        return {"emoji": "🥇", "label": "Parfait!", "dioula": "I ye a kɛ fɛnkolo la!"}
    elif percentage >= 80:
        return {"emoji": "🥈", "label": "Très bien!", "dioula": "I ye a kɛ ka ɲɛ!"}
    elif percentage >= 60:
        return {"emoji": "🥉", "label": "Bien!", "dioula": "I ye a kɛ!"}
    else:
        return {"emoji": "📚", "label": "Continue!", "dioula": "I kana to!"}