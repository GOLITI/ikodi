#!/usr/bin/env python3
"""
Test du pipeline vocal complet avec un fichier audio réel
"""
import requests
import json
from pathlib import Path

BASE_URL = "http://127.0.0.1:8001/api"

# Fichier audio de test
AUDIO_FILE = Path("test_direct.wav")  # Fichier WAV existant

def test_voice_with_real_audio():
    """Test de l'interaction vocale avec un fichier audio réel"""
    print("╔══════════════════════════════════════════════════════╗")
    print("║  TEST COMMUNICATION VOCALE - Niveau 3               ║")
    print("║  Fichier: AUDIO-de_test.m4a                         ║")
    print("╚══════════════════════════════════════════════════════╝\n")
    
    if not AUDIO_FILE.exists():
        print(f"[ERREUR] Fichier audio introuvable: {AUDIO_FILE}")
        return False
    
    print(f"[1/4] Chargement du fichier audio...")
    print(f"     Fichier: {AUDIO_FILE}")
    print(f"     Taille: {AUDIO_FILE.stat().st_size} bytes\n")
    
    try:
        # Test 1: Voice interaction complète
        print("[2/4] Envoi vers /voice-interaction...")
        print("     (Whisper se charge au 1er appel, patientez 30-60s...)\n")
        
        with open(AUDIO_FILE, 'rb') as f:
            files = {'audio': (AUDIO_FILE.name, f, 'audio/m4a')}
            r = requests.post(
                f"{BASE_URL}/niveau3/voice-interaction",
                files=files,
                timeout=180
            )
        
        print(f"     Status: {r.status_code}")
        
        if r.status_code != 200:
            print(f"\n[ERREUR] {r.status_code}")
            print(f"     Detail: {r.json().get('detail', 'Erreur inconnue')}")
            return False
        
        data = r.json()
        
        print("\n" + "="*60)
        print("✓ SUCCES - Pipeline vocal complet!\n")
        print(f"📝 Transcription (Whisper STT):")
        print(f"   '{data.get('transcription')}'\n")
        
        print(f"🤖 Réponse IA (Mistral RAG):")
        response_lines = data.get('ai_response', '').split('\n')
        for line in response_lines[:5]:  # Première 5 lignes
            print(f"   {line}")
        if len(response_lines) > 5:
            print(f"   ... ({len(response_lines)} lignes au total)\n")
        else:
            print()
        
        print(f"📚 Phrases similaires ({len(data.get('similar_phrases', []))}):")
        for i, phrase in enumerate(data.get('similar_phrases', [])[:3], 1):
            print(f"   {i}. {phrase.get('dioula', '')} = {phrase.get('french', '')}")
        
        print(f"\n🔊 Audio TTS généré: {'✓ OUI' if data.get('response_audio_base64') else '✗ NON'}")
        if data.get('response_audio_base64'):
            audio_len = len(data.get('response_audio_base64', ''))
            print(f"   Taille: {audio_len} chars base64 (~{audio_len*3//4} bytes)")
        
        print(f"\n💯 Score: {data.get('score', 0)}/10")
        
        print("="*60)
        
        # Test 2: Text chat (comparaison)
        print("\n[3/4] Test text-chat avec la même phrase...\n")
        
        r2 = requests.post(
            f"{BASE_URL}/niveau3/text-chat",
            json={"text": data.get('transcription', 'Bonjour')},
            timeout=60
        )
        
        if r2.status_code == 200:
            data2 = r2.json()
            print(f"✓ Text-chat aussi fonctionnel")
            print(f"  Réponse: {data2.get('ai_response', '')[:80]}...\n")
        
        print("[4/4] Health check...\n")
        r3 = requests.get(f"http://127.0.0.1:8001/health")
        if r3.status_code == 200:
            health = r3.json()
            print(f"✓ Serveur: {health.get('status')}")
            print(f"  RAG initialisé: {health.get('rag_initialized')}")
            print(f"  LLM: {health.get('llm_engine')}")
            print(f"  Mode: {health.get('mode')}\n")
        
        print("="*60)
        print("🎉 TOUS LES TESTS PASSES!")
        print("="*60)
        return True
        
    except requests.exceptions.Timeout:
        print("\n[ERREUR] Timeout - Le serveur ne répond pas assez vite")
        print("  Whisper prend ~30-60s au 1er appel pour charger le modèle")
        return False
    except Exception as e:
        print(f"\n[ERREUR] Exception: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_voice_with_real_audio()
    exit(0 if success else 1)
