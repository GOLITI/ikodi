"""
Script de test des endpoints spécialisés : proverbes vs contes
================================================================

Usage:
    1. Démarrer l'API : python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
    2. Exécuter ce test : python test_endpoints.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def tester_endpoint_proverbe():
    """Test de l'endpoint /ask/proverbe"""
    print("\n" + "="*60)
    print("🔵 TEST : /ask/proverbe")
    print("="*60)
    
    payload = {
        "question": "Comment gérer les conflits familiaux ?",
        "nb_resultats": 3
    }
    
    response = requests.post(f"{BASE_URL}/ask/proverbe", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Question : {data['question']}")
        print(f"\n📖 Réponse :\n{data['reponse'][:300]}...")
        print(f"\n📚 Sources ({data['nb_sources']}) :")
        for i, src in enumerate(data['sources'], 1):
            print(f"  {i}. [{src['ethnie']}] {src.get('titre_parent', 'Sans titre')}")
            print(f"     Type: {src['type_contenu']} | Score: {src['score']:.3f}")
            # Vérification que ce sont bien des proverbes
            assert src['type_contenu'] == 'proverbe', f"❌ Erreur : conte trouvé dans /ask/proverbe!"
        print("\n✅ Tous les résultats sont bien des PROVERBES")
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")


def tester_endpoint_conte():
    """Test de l'endpoint /ask/conte"""
    print("\n" + "="*60)
    print("🟢 TEST : /ask/conte")
    print("="*60)
    
    payload = {
        "question": "Raconte-moi l'histoire de Yakouba et le lion",
        "nb_resultats": 3
    }
    
    response = requests.post(f"{BASE_URL}/ask/conte", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Question : {data['question']}")
        print(f"\n📖 Réponse :\n{data['reponse'][:300]}...")
        print(f"\n📚 Sources ({data['nb_sources']}) :")
        for i, src in enumerate(data['sources'], 1):
            print(f"  {i}. [{src['ethnie']}] {src.get('titre_parent', 'Sans titre')}")
            print(f"     Type: {src['type_contenu']} | Score: {src['score']:.3f}")
            if src.get('morale'):
                print(f"     Morale: {src['morale'][:60]}...")
            # Vérification que ce sont bien des contes
            assert src['type_contenu'] == 'conte', f"❌ Erreur : proverbe trouvé dans /ask/conte!"
        print("\n✅ Tous les résultats sont bien des CONTES")
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")


def tester_endpoint_simple():
    """Test de l'endpoint /ask/simple (mixte)"""
    print("\n" + "="*60)
    print("🟡 TEST : /ask/simple (mixte)")
    print("="*60)
    
    payload = {
        "question": "Comment faire preuve de courage ?",
        "nb_resultats": 5
    }
    
    response = requests.post(f"{BASE_URL}/ask/simple", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Question : {data['question']}")
        print(f"\n📖 Réponse :\n{data['reponse'][:300]}...")
        print(f"\n📚 Sources ({data['nb_sources']}) :")
        
        types_trouves = set()
        for i, src in enumerate(data['sources'], 1):
            print(f"  {i}. [{src['ethnie']}] {src.get('titre_parent', 'Sans titre')}")
            print(f"     Type: {src['type_contenu']} | Score: {src['score']:.3f}")
            types_trouves.add(src['type_contenu'])
        
        print(f"\n✅ Types trouvés : {', '.join(types_trouves)}")
        print("   (L'endpoint /ask/simple peut retourner contes ET proverbes)")
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")


if __name__ == "__main__":
    print("\n" + "🥁"*30)
    print("TEST DES ENDPOINTS SPÉCIALISÉS - GriotKnowledge API")
    print("🥁"*30)
    
    try:
        # Test de la santé de l'API
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        if health.status_code != 200:
            print("❌ L'API n'est pas disponible. Démarrez-la avec :")
            print("   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000")
            exit(1)
        
        print("✅ API opérationnelle\n")
        
        # Tests des endpoints
        tester_endpoint_proverbe()
        tester_endpoint_conte()
        tester_endpoint_simple()
        
        print("\n" + "="*60)
        print("✅ TOUS LES TESTS RÉUSSIS !")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Impossible de se connecter à l'API.")
        print("   Démarrez-la avec : python -m uvicorn app.main:app --host 127.0.0.1 --port 8000\n")
    except Exception as e:
        print(f"\n❌ Erreur : {e}\n")
