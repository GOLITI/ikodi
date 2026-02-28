import os
from typing import List, Dict

def load_dioula_pairs(max_samples: int = 500) -> List[Dict]:
    """
    Charge les paires dioula-français depuis HuggingFace.
    Dataset: uvci/Koumankan_mt_dyu_fr
    """
    try:
        from datasets import load_dataset
        dataset = load_dataset(
            "uvci/Koumankan_mt_dyu_fr",
            token=os.getenv("HUGGINGFACE_TOKEN"),
            split="train"
        )
        
        pairs = []
        for i, row in enumerate(dataset):
            if i >= max_samples:
                break
            # Structure: {'ID': '...', 'translation': {'dyu': '...', 'fr': '...'}}
            translation = row.get("translation", {})
            dioula = translation.get("dyu", "")
            french = translation.get("fr", "")
            if dioula and french:
                pairs.append({
                    "dioula": dioula,
                    "french": french,
                    "id": i
                })
        
        print(f"[OK] {len(pairs)} paires Dioula-Francais chargees depuis HuggingFace")
        return pairs
    
    except Exception as e:
        print(f"[WARN] Erreur chargement dataset HuggingFace: {e}")
        print("[INFO] Utilisation des donnees de fallback...")
        return get_fallback_data()


def get_fallback_data() -> List[Dict]:
    """Données de base si le dataset est inaccessible"""
    return [
        {"dioula": "I ni ce", "french": "Bonjour / Salut", "id": 0},
        {"dioula": "I ni sogoma", "french": "Bonjour (le matin)", "id": 1},
        {"dioula": "I ni wula", "french": "Bonsoir", "id": 2},
        {"dioula": "Aw ni ce", "french": "Bonjour (pluriel)", "id": 3},
        {"dioula": "Fo!", "french": "Salut!", "id": 4},
        {"dioula": "N togo ye...", "french": "Je m'appelle...", "id": 5},
        {"dioula": "I togo ye di?", "french": "Comment tu t'appelles?", "id": 6},
        {"dioula": "N be di", "french": "Je vais bien", "id": 7},
        {"dioula": "I be di wa?", "french": "Comment tu vas?", "id": 8},
        {"dioula": "N baro", "french": "Mon ami", "id": 9},
        {"dioula": "I kana balo", "french": "Ne t'inquiète pas", "id": 10},
        {"dioula": "A ye di", "french": "C'est bon / C'est bien", "id": 11},
        {"dioula": "Nba", "french": "Mère", "id": 12},
        {"dioula": "Fa", "french": "Père", "id": 13},
        {"dioula": "Dɔgɔ", "french": "Petit frère / Petite sœur", "id": 14},
        {"dioula": "Kɔrɔ", "french": "Grand frère / Grande sœur", "id": 15},
        {"dioula": "Den", "french": "Enfant", "id": 16},
        {"dioula": "Jɔ!", "french": "Arrête!", "id": 17},
        {"dioula": "Taa!", "french": "Va-t'en / Pars!", "id": 18},
        {"dioula": "Na!", "french": "Viens!", "id": 19},
        {"dioula": "A ye baara kɛ", "french": "Il/Elle a travaillé", "id": 20},
        {"dioula": "Ne bɛ taa sugu la", "french": "Je vais au marché", "id": 21},
        {"dioula": "Dugu kɔnɔ", "french": "Dans le village", "id": 22},
        {"dioula": "Sɔrɔ", "french": "Obtenir / Trouver", "id": 23},
        {"dioula": "Kɛ", "french": "Faire", "id": 24},
        {"dioula": "Taa", "french": "Aller", "id": 25},
        {"dioula": "Na", "french": "Venir", "id": 26},
        {"dioula": "Sɔrɔ", "french": "Avoir / Obtenir", "id": 27},
        {"dioula": "Dɔ", "french": "Un peu / Quelque chose", "id": 28},
        {"dioula": "Bɛɛ", "french": "Tout / Tous", "id": 29},
        {"dioula": "A man di", "french": "Ce n'est pas bien", "id": 30},
        {"dioula": "I ni baara", "french": "Bravo pour ton travail", "id": 31},
        {"dioula": "Aw ni baara", "french": "Bravo pour votre travail", "id": 32},
        {"dioula": "Koɲuman", "french": "Bonne chose / C'est bon", "id": 33},
        {"dioula": "Kojugu", "french": "Mauvaise chose / C'est mauvais", "id": 34},
        {"dioula": "Bi", "french": "Aujourd'hui", "id": 35},
        {"dioula": "Sini", "french": "Demain", "id": 36},
        {"dioula": "Kunu", "french": "Hier", "id": 37},
        {"dioula": "Tile", "french": "Soleil / Jour", "id": 38},
        {"dioula": "Su", "french": "Nuit", "id": 39},
        {"dioula": "Ji", "french": "Eau", "id": 40},
        {"dioula": "Misi", "french": "Vache", "id": 41},
        {"dioula": "Wulu", "french": "Chien", "id": 42},
        {"dioula": "Donkili", "french": "Chanson / Chant", "id": 43},
        {"dioula": "Fɔ", "french": "Dire / Jouer (instrument)", "id": 44},
        {"dioula": "Bolo", "french": "Main / Bras", "id": 45},
        {"dioula": "Ulu", "french": "Eux / Ils", "id": 46},
        {"dioula": "An", "french": "Nous", "id": 47},
        {"dioula": "Aw", "french": "Vous", "id": 48},
        {"dioula": "A", "french": "Il / Elle", "id": 49},
    ]
