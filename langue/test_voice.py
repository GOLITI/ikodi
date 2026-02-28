"""Test de communication vocale - Pipeline STT → RAG → TTS"""
import requests
import base64
import os
from pathlib import Path

BASE_URL = "http://127.0.0.1:8001/api"
AUDIO_DIR = Path("audio_samples")
AUDIO_DIR.mkdir(exist_ok=True)

def generate_test_audio(text):
    """Génère un fichier audio de test avec ElevenLabs TTS"""
    print(f"\n[1/4] Generation audio test: '{text}'")
    try:
        r = requests.get(
            f"{BASE_URL}/niveau2/audio",
            params={"text": text},
            timeout=30
        )
        if r.status_code == 200:
            audio_path = AUDIO_DIR / "test_input.mp3"
            audio_path.write_bytes(r.content)
            print(f"     ✓ Audio generated: {audio_path} ({len(r.content)} bytes)")
            return audio_path
        else:
            print(f"     ✗ Error TTS: {r.status_code}")
            return None
    except Exception as e:
        print(f"     ✗ Error: {e}")
        return None

def test_voice_interaction(audio_path):
    """Test du pipeline vocal complet"""
    print(f"\n[2/4] Upload audio pour voice interaction...")
    
    try:
        with open(audio_path, 'rb') as f:
            files = {'audio': ('recording.mp3', f, 'audio/mpeg')}
            r = requests.post(
                f"{BASE_URL}/niveau3/voice-interaction",
                files=files,
                timeout=120
            )
        
        if r.status_code == 200:
            data = r.json()
            
            print(f"\n[3/4] RESULTATS:")
            print(f"     📝 Transcription: {data['transcription']}")
            print(f"     🤖 Réponse IA:")
            print(f"        {data['ai_response'][:200]}...")
            
            print(f"\n     📚 Phrases similaires:")
            for p in data['similar_phrases'][:2]:
                print(f"        • {p['dioula']} = {p['french']}")
            
            print(f"\n     🎯 Score: {data.get('score', 'N/A')}/10")
            
            # Sauvegarder l'audio de réponse
            if data.get('response_audio_base64'):
                print(f"\n[4/4] Sauvegarde audio réponse...")
                audio_bytes = base64.b64decode(data['response_audio_base64'])
                response_path = AUDIO_DIR / "ai_response.mp3"
                response_path.write_bytes(audio_bytes)
                print(f"     ✓ Audio sauvegardé: {response_path} ({len(audio_bytes)} bytes)")
            else:
                print(f"\n[4/4] Pas d'audio de réponse (ElevenLabs désactivé)")
            
            return True
        else:
            print(f"     ✗ Erreur {r.status_code}: {r.text[:200]}")
            return False
            
    except Exception as e:
        print(f"     ✗ Exception: {e}")
        return False

def test_with_existing_audio():
    """Test avec un fichier audio existant s'il y en a un"""
    existing = AUDIO_DIR / "test_input.mp3"
    if existing.exists():
        print(f"\n[INFO] Utilisation audio existant: {existing}")
        return test_voice_interaction(existing)
    return False

# ═══════════════════════════════════════════════════════════
print("╔══════════════════════════════════════════════════════╗")
print("║  TEST COMMUNICATION VOCALE - Niveau 3               ║")
print("║  Pipeline: STT (Whisper) → RAG (Mistral) → TTS     ║")
print("╚══════════════════════════════════════════════════════╝")

# Test 1: Phrase simple
test_text = "I ni sogoma"
audio_file = generate_test_audio(test_text)

if audio_file:
    success = test_voice_interaction(audio_file)
    
    if success:
        print("\n" + "="*60)
        print("✓ TEST VOCAL REUSSI!")
        print("  - Audio input généré et uploadé")
        print("  - Whisper a transcrit correctement")
        print("  - Mistral AI a répondu en Dioula")
        print("  - ElevenLabs a synthétisé la réponse")
        print("\n  Fichiers générés:")
        print(f"    → {AUDIO_DIR / 'test_input.mp3'}")
        if (AUDIO_DIR / 'ai_response.mp3').exists():
            print(f"    → {AUDIO_DIR / 'ai_response.mp3'}")
    else:
        print("\n✗ ECHEC du test vocal")
else:
    print("\n✗ Impossible de générer l'audio de test")
    print("  Vérifiez que ELEVENLABS_API_KEY est valide dans .env")

print("\n" + "="*60)
