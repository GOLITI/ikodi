"""Test de conversation en Dioula avec l'IA Mistral via Niveau 3"""
import requests
import json

BASE = "http://127.0.0.1:8001/api/niveau3/text-chat"

def chat(message):
    """Envoie un message et affiche la réponse"""
    print(f"\n👤 USER: {message}")
    try:
        r = requests.post(BASE, json={"text": message}, timeout=60)
        if r.status_code == 200:
            data = r.json()
            print(f"🤖 AI: {data['ai_response']}")
            if data.get('similar_phrases'):
                print("\n📚 Phrases similaires du corpus:")
                for p in data['similar_phrases'][:2]:
                    print(f"   • {p['dioula']}  =  {p['french']}")
        else:
            print(f"❌ Erreur: {r.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

# ═══════════════════════════════════════════════════════════
print("╔══════════════════════════════════════════════════════╗")
print("║  TEST CONVERSATION DIOULA - MISTRAL AI              ║")
print("╚══════════════════════════════════════════════════════╝")

# Conversation 1: Salutations
chat("I ni sogoma! Comment tu t'appelles?")

# Conversation 2: Apprentissage
chat("Je suis débutant. Comment dire je m'appelle en Dioula?")

# Conversation 3: Famille
chat("Comment on dit ma mère en Dioula?")

# Conversation 4: Question avancée
chat("Explique-moi la différence entre I ni ce et An bena laba")

# Conversation 5: Culture
chat("C'est quoi l'importance du Dioula en Côte d'Ivoire?")

print("\n" + "="*60)
print("Test de conversation terminé!")
