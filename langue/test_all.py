"""Test all 3 levels of the Dioula microservice."""
import requests, json, time, base64
from pathlib import Path

BASE = "http://127.0.0.1:8001/api"
HEALTH = "http://127.0.0.1:8001/health"
OK = 0
FAIL = 0

def test(name, func):
    global OK, FAIL
    try:
        func()
        print(f"  ✅ {name}")
        OK += 1
    except Exception as e:
        print(f"  ❌ {name}: {e}")
        FAIL += 1

# ============ HEALTH ============
print("\n🏥 HEALTH")
def t_health():
    r = requests.get(HEALTH)
    assert r.status_code == 200
    d = r.json()
    assert d["status"] == "ok"
    assert d["rag_initialized"] == True
    print(f"     mode={d['mode']}, llm={d['llm_engine']}")
test("Health check", t_health)

# ============ NIVEAU 1 ============
print("\n📚 NIVEAU 1 — Texte + Quiz")

def t_lessons():
    r = requests.get(f"{BASE}/niveau1/lessons")
    assert r.status_code == 200
    d = r.json()
    assert d["total"] == 6
    for l in d["lessons"]:
        print(f"     Leçon {l['id']}: {l['title']} ({l['phrase_count']} phrases, {l['quiz_count']} quiz)")
test("Lessons list", t_lessons)

def t_lesson_detail():
    r = requests.get(f"{BASE}/niveau1/lessons/1")
    assert r.status_code == 200
    d = r.json()
    assert "vocabulary" in d
    print(f"     Leçon 1: {len(d['vocabulary'])} mots")
test("Lesson 1 detail", t_lesson_detail)

def t_quiz():
    r = requests.get(f"{BASE}/niveau1/lessons/1/quiz")
    assert r.status_code == 200
    d = r.json()
    assert len(d) > 0
    print(f"     {len(d)} questions, Q1: {d[0]['question'][:60]}...")
test("Quiz leçon 1", t_quiz)

def t_check_correct():
    # Get quiz first  
    r = requests.get(f"{BASE}/niveau1/lessons/1/quiz")
    quiz = r.json()
    q = quiz[0]
    # Try to find correct answer
    r2 = requests.post(f"{BASE}/niveau1/lessons/1/quiz/check", json={
        "question_index": 0,
        "answer": q["options"][0]
    })
    assert r2.status_code == 200
    d = r2.json()
    print(f"     correct={d.get('correct')}, score={d.get('score')}")
test("Quiz check answer", t_check_correct)

def t_search():
    r = requests.get(f"{BASE}/niveau1/search", params={"q": "bonjour"})
    assert r.status_code == 200
    d = r.json()
    print(f"     Found {len(d.get('results', []))} results for 'bonjour'")
test("Search 'bonjour'", t_search)

def t_ask():
    r = requests.post(f"{BASE}/niveau1/ask", json={"question": "Comment dit-on merci en Dioula?"})
    assert r.status_code == 200
    d = r.json()
    ans = d.get("answer", d.get("response", ""))
    print(f"     Answer: {ans[:100]}...")
test("Ask AI question", t_ask)

# ============ NIVEAU 2 ============
print("\n🔊 NIVEAU 2 — Texte + Audio")

def t_phrases():
    r = requests.get(f"{BASE}/niveau2/phrases")
    assert r.status_code == 200
    d = r.json()
    phrases = d if isinstance(d, list) else d.get("phrases", [])
    print(f"     {len(phrases)} phrases")
    if phrases:
        p = phrases[0]
        print(f"     P1: {p.get('dioula', '')} = {p.get('french', p.get('francais', ''))}")
test("Phrases list", t_phrases)

def t_audio():
    r = requests.post(f"{BASE}/niveau2/audio", json={"text": "I ni ce", "language": "fr"})
    print(f"     Status: {r.status_code}")
    if r.status_code == 200:
        ct = r.headers.get("content-type", "")
        print(f"     Content-Type: {ct}, Size: {len(r.content)} bytes")
    else:
        d = r.json() if r.headers.get("content-type","").startswith("application/json") else {}
        print(f"     Error: {d.get('detail', r.text[:200])}")
test("Audio TTS (ElevenLabs)", t_audio)

# ============ NIVEAU 3 ============
print("\n🎤 NIVEAU 3 — Interaction vocale & IA")

def t_text_chat():
    r = requests.post(f"{BASE}/niveau3/text-chat", json={"text": "I ni ce"}, timeout=60)
    assert r.status_code == 200
    d = r.json()
    resp = d.get("ai_response", d.get("response", ""))
    print(f"     Réponse IA: {resp[:80]}...")
    
    # Vérifier l'audio généré
    audio_b64 = d.get("response_audio_base64")
    if audio_b64:
        audio_bytes = base64.b64decode(audio_b64)
        print(f"     ✓ Audio TTS: {len(audio_bytes)} bytes")
        
        # Sauvegarder pour vérification
        output = Path("audio_samples/test_niveau3_ia.mp3")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(audio_bytes)
        print(f"     Sauvegardé: {output}")
    else:
        print(f"     ⚠ Pas d'audio (vérifier ElevenLabs API)")
test("Text chat avec audio IA", t_text_chat)

# ============ SUMMARY ============
print(f"\n{'='*50}")
print(f"📊 RESULTS: {OK} passed, {FAIL} failed out of {OK+FAIL} tests")
if FAIL == 0:
    print("🎉 All tests passed!")
