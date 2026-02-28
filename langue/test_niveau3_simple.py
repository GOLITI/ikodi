#!/usr/bin/env python3
"""
Test rapide du Niveau 3 - IA vocale avec Mistral + ElevenLabs
"""
import requests
import base64
import json
from pathlib import Path

BASE_URL = "http://127.0.0.1:8001/api"

def test_niveau3_text_chat():
    """Test du chat textuel avec génération audio"""
    print("="*60)
    print("TEST NIVEAU 3 - IA DIOULA + AUDIO")
    print("="*60)
    
    # Test 1: Chat textuel avec réponse audio
    print("\n[1] Test text-chat avec génération audio...")
    print("   Question: 'Comment dire bonjour en Dioula?'")
    
    try:
        r = requests.post(
            f"{BASE_URL}/niveau3/text-chat",
            json={"text": "Comment dire bonjour en Dioula?"},
            timeout=60
        )
        
        if r.status_code != 200:
            print(f"   ✗ ERREUR {r.status_code}: {r.text}")
            return False
        
        data = r.json()
        
        print(f"\n   ✓ Réponse IA (Mistral):")
        response_text = data.get('ai_response', '')
        for line in response_text.split('\n')[:5]:
            print(f"     {line}")
        
        print(f"\n   Phrases similaires: {len(data.get('similar_phrases', []))} trouvées")
        for phrase in data.get('similar_phrases', [])[:2]:
            print(f"     • {phrase.get('dioula')} = {phrase.get('french')}")
        
        # Vérifier l'audio
        audio_b64 = data.get('response_audio_base64')
        if audio_b64:
            audio_size = len(audio_b64) * 3 // 4  # Taille approximative en bytes
            print(f"\n   ✓ Audio TTS généré par ElevenLabs!")
            print(f"     Taille: ~{audio_size} bytes")
            
            # Sauvegarder l'audio pour vérification
            audio_bytes = base64.b64decode(audio_b64)
            output_file = Path("audio_samples/niveau3_response.mp3")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_bytes(audio_bytes)
            print(f"     Sauvegardé: {output_file}")
        else:
            print(f"\n   ✗ AUCUN audio généré (ElevenLabs ne répond pas?)")
            return False
        
        print("\n" + "="*60)
        print("✓ NIVEAU 3 FONCTIONNEL!")
        print("  • Mistral AI génère des réponses en Dioula")
        print("  • ElevenLabs génère l'audio de la réponse")
        print("  • Recherche sémantique dans le corpus")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n   ✗ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_health():
    """Vérification santé du serveur"""
    print("\n[2] Health check...")
    try:
        r = requests.get("http://127.0.0.1:8001/health", timeout=5)
        if r.status_code == 200:
            data = r.json()
            print(f"   Status: {data.get('status')}")
            print(f"   RAG: {data.get('rag_initialized')}")
            print(f"   LLM: {data.get('llm_engine')}")
            print(f"   Mode: {data.get('mode')}")
            return True
    except:
        print("   ✗ Serveur non disponible sur http://127.0.0.1:8001")
        return False


if __name__ == "__main__":
    print("\n🎤 TEST MICROSERVICE DIOULA - NIVEAU 3\n")
    
    if not test_health():
        print("\n⚠️  Démarrez d'abord le serveur:")
        print("   .\\venv\\Scripts\\uvicorn.exe app.main:app --host 127.0.0.1 --port 8001")
        exit(1)
    
    success = test_niveau3_text_chat()
    
    if success:
        print("\n🎉 SUCCÈS - Le niveau 3 est opérationnel!")
        print("\n📝 Note: Pour tester la reconnaissance vocale (Whisper),")
        print("   il faudrait installer ffmpeg sur Windows.")
        print("   Pour l'instant, l'IA peut:")
        print("   • Répondre en Dioula (Mistral AI)")
        print("   • Générer l'audio (ElevenLabs TTS)")
        print("   • Chercher dans le corpus (ChromaDB)")
    else:
        print("\n❌ Le test a échoué - Vérifiez:")
        print("   • Le serveur tourne sur le port 8001")
        print("   • La clé API Mistral est valide")
        print("   • La clé API ElevenLabs est valide")
    
    exit(0 if success else 1)
