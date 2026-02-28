"""Test de communication vocale - Alternative sans ElevenLabs pour audio input"""
import requests
import base64
import wave
import struct
import math
from pathlib import Path

BASE_URL = "http://127.0.0.1:8001/api"
AUDIO_DIR = Path("audio_samples")
AUDIO_DIR.mkdir(exist_ok=True)

def create_synthetic_audio():
    """Crée un fichier audio WAV synthétique (tone à 440Hz pendant 1s)"""
    print(f"\n[1/4] Creation audio synthetique pour test...")
    
    sample_rate = 16000  # Whisper préfère 16kHz
    duration = 1.0
    frequency = 440.0  # A4 note
    
    num_samples = int(sample_rate * duration)
    
    # Générer un ton sinusoïdal
    samples = []
    for i in range(num_samples):
        sample = int(32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
        samples.append(sample)
    
    # Créer le fichier WAV
    audio_path = AUDIO_DIR / "test_synthetic.wav"
    with wave.open(str(audio_path), 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(struct.pack('<%dh' % len(samples), *samples))
    
    print(f"     ✓ Audio synthetique cree: {audio_path}")
    return audio_path

def test_voice_interaction(audio_path):
    """Test du pipeline vocal complet"""
    print(f"\n[2/4] Upload audio: {audio_path.name}")
    print(f"     Taille: {audio_path.stat().st_size} bytes")
    
    try:
        with open(audio_path, 'rb') as f:
            files = {'audio': (audio_path.name, f, 'audio/wav')}
            print(f"\n     Envoi vers /voice-interaction...")
            print(f"     (Whisper se charge au 1er appel, patientez 30-60s...)")
            r = requests.post(
                f"{BASE_URL}/niveau3/voice-interaction",
                files=files,
                timeout=300  # 5 minutes pour le 1er appel (chargement Whisper)
            )
        
        print(f"     Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            
            print(f"\n[3/4] ✓ RESULTATS:")
            print(f"     📝 Transcription Whisper: '{data['transcription']}'")
            
            print(f"\n     🤖 Reponse IA Mistral:")
            response = data['ai_response']
            lines = response.split('\n')
            for line in lines[:5]:  # Premières 5 lignes
                print(f"        {line}")
            if len(lines) > 5:
                print(f"        ... ({len(lines)-5} lignes de plus)")
            
            print(f"\n     📚 Phrases similaires du corpus:")
            for i, p in enumerate(data['similar_phrases'][:3], 1):
                print(f"        {i}. {p['dioula']} = {p['french']}")
            
            print(f"\n     🎯 Score prononciation: {data.get('score', 'N/A')}/10")
            
            # Audio de réponse
            print(f"\n[4/4] Audio reponse:")
            if data.get('response_audio_base64'):
                audio_bytes = base64.b64decode(data['response_audio_base64'])
                response_path = AUDIO_DIR / "ai_response.mp3"
                response_path.write_bytes(audio_bytes)
                print(f"     ✓ Audio TTS sauvegarde: {response_path}")
                print(f"     Taille: {len(audio_bytes)} bytes")
            else:
                print(f"     ⚠ Pas d'audio TTS (ElevenLabs desactive ou erreur)")
            
            return True
        else:
            print(f"\n[ERREUR] {r.status_code}")
            try:
                error = r.json()
                print(f"     Detail: {error.get('detail', r.text[:300])}")
            except:
                print(f"     {r.text[:300]}")
            return False
            
    except Exception as e:
        print(f"\n[EXCEPTION] {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_stt():
    """Test simple de Whisper STT uniquement"""
    print(f"\n[TEST SIMPLE] Verification que Whisper fonctionne...")
    audio_path = create_synthetic_audio()
    
    if audio_path and audio_path.exists():
        with open(audio_path, 'rb') as f:
            files = {'audio': (audio_path.name, f, 'audio/wav')}
            try:
                r = requests.post(
                    f"{BASE_URL}/niveau3/voice-interaction",
                    files=files,
                    timeout=60
                )
                print(f"     Status: {r.status_code}")
                if r.status_code == 200:
                    print(f"     ✓ Whisper a transcrit: '{r.json()['transcription']}'")
                    return True
                else:
                    print(f"     ✗ Erreur: {r.text[:200]}")
            except Exception as e:
                print(f"     ✗ Exception: {e}")
    return False

# ═══════════════════════════════════════════════════════════
print("╔══════════════════════════════════════════════════════╗")
print("║  TEST COMMUNICATION VOCALE - Niveau 3               ║")
print("║  Pipeline: STT (Whisper) → RAG (Mistral) → TTS     ║")
print("╚══════════════════════════════════════════════════════╝")

print("\n[INFO] Test avec audio synthetique (ElevenLabs non requis)")

# Créer audio de test
audio_file = create_synthetic_audio()

if audio_file and audio_file.exists():
    success = test_voice_interaction(audio_file)
    
    print("\n" + "="*60)
    if success:
        print("✓ PIPELINE VOCAL TESTE AVEC SUCCES!")
        print("\n  Composants valides:")
        print("    ✓ Upload multipart/form-data")
        print("    ✓ Whisper STT (transcription)")
        print("    ✓ Mistral RAG (reponse IA)")
        print("    ✓ ChromaDB (phrases similaires)")
        print("    ? ElevenLabs TTS (depend de la cle API)")
        
        print(f"\n  Fichiers generes dans {AUDIO_DIR}:")
        for f in AUDIO_DIR.glob("*"):
            print(f"    → {f.name} ({f.stat().st_size} bytes)")
    else:
        print("✗ ECHEC du pipeline vocal")
        print("\n  Verifications:")
        print("    - Whisper est-il installe? (pip install openai-whisper)")
        print("    - Le serveur est-il actif? (http://127.0.0.1:8001)")
        print("    - Mistral API key est valide?")
else:
    print("\n✗ Impossible de creer l'audio de test")

print("="*60)
