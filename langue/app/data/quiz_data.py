# app/data/quiz_data.py
# Données statiques pour le Niveau 1 (Texte + Quiz)
# Aucune API requise — fonctionne sans clé

NIVEAU1_LESSONS = [
    # ── Leçon 1 : Salutations ────────────────────────────────
    {
        "id": 1,
        "title": "Les Salutations",
        "theme": "greetings",
        "emoji": "👋",
        "description": "Apprenez à saluer en Dioula, la langue du peuple Dioula de Côte d'Ivoire",
        "content": [
            {
                "dioula": "I ni ce",
                "french": "Bonjour / Salut",
                "context": "Salutation générale (toute la journée)",
                "phonetic": "i ni ssé",
            },
            {
                "dioula": "I ni sogoma",
                "french": "Bonjour du matin",
                "context": "Utilisé uniquement le matin",
                "phonetic": "i ni so-go-ma",
            },
            {
                "dioula": "I ni wula",
                "french": "Bonsoir",
                "context": "Le soir après le coucher du soleil",
                "phonetic": "i ni ou-la",
            },
            {
                "dioula": "Aw ni ce",
                "french": "Bonjour à vous (groupe)",
                "context": "Pour saluer plusieurs personnes en même temps",
                "phonetic": "aw ni ssé",
            },
            {
                "dioula": "I be di wa?",
                "french": "Comment tu vas ?",
                "context": "Demander des nouvelles à quelqu'un",
                "phonetic": "i bé di oua",
            },
            {
                "dioula": "N be di",
                "french": "Je vais bien",
                "context": "Réponse positive — tout va bien",
                "phonetic": "n bé di",
            },
            {
                "dioula": "Fo!",
                "french": "Salut ! (informel)",
                "context": "Entre amis, de façon décontractée",
                "phonetic": "fo",
            },
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "Comment dit-on 'Bonjour' en Dioula (salutation générale) ?",
                "options": ["I ni ce", "N be di", "Taa!", "Fo!"],
                "correct": 0,
                "explanation": "'I ni ce' est la salutation universelle en Dioula, utilisable à toute heure de la journée.",
            },
            {
                "id": "q2",
                "question": "Que signifie 'I be di wa?' ?",
                "options": ["Je m'appelle...", "Au revoir", "Comment tu vas ?", "Merci beaucoup"],
                "correct": 2,
                "explanation": "'I be di wa?' est la façon courante de demander 'comment vas-tu?' en Dioula.",
            },
            {
                "id": "q3",
                "question": "Comment répondre positivement à 'I be di wa?' ?",
                "options": ["Taa!", "N be di", "I ni wula", "Jɔ!"],
                "correct": 1,
                "explanation": "'N be di' signifie 'je vais bien'. C'est la réponse standard et polie.",
            },
            {
                "id": "q4",
                "question": "Quelle salutation utilise-t-on le matin ?",
                "options": ["I ni wula", "I ni ce", "I ni sogoma", "Aw ni ce"],
                "correct": 2,
                "explanation": "'I ni sogoma' est spécifiquement la salutation du matin en Dioula.",
            },
            {
                "id": "q5",
                "question": "Comment saluer un groupe de personnes en Dioula ?",
                "options": ["I ni ce", "Aw ni ce", "N be di", "Fo!"],
                "correct": 1,
                "explanation": "'Aw ni ce' utilise le pronom pluriel 'Aw' (vous) pour saluer plusieurs personnes.",
            },
        ],
    },

    # ── Leçon 2 : La Famille ─────────────────────────────────
    {
        "id": 2,
        "title": "La Famille",
        "theme": "family",
        "emoji": "👨‍👩‍👧‍👦",
        "description": "Les membres de la famille en Dioula — valeurs fondamentales de la culture ivoirienne",
        "content": [
            {
                "dioula": "Nba",
                "french": "Mère",
                "context": "La mère, figure centrale de la famille ivoirienne",
                "phonetic": "n-ba",
            },
            {
                "dioula": "Fa",
                "french": "Père",
                "context": "Le père, chef de famille traditionnellement",
                "phonetic": "fa",
            },
            {
                "dioula": "Dɔgɔ",
                "french": "Petit frère / Petite sœur (cadet)",
                "context": "Désigne le plus jeune dans la fratrie",
                "phonetic": "dɔ-gɔ",
            },
            {
                "dioula": "Kɔrɔ",
                "french": "Grand frère / Grande sœur (aîné)",
                "context": "Désigne le plus âgé dans la fratrie — figure de respect",
                "phonetic": "kɔ-rɔ",
            },
            {
                "dioula": "Den",
                "french": "Enfant",
                "context": "Tout enfant, garçon ou fille",
                "phonetic": "dèn",
            },
            {
                "dioula": "Ke",
                "french": "Homme / Mari",
                "context": "Genre masculin ou époux",
                "phonetic": "ké",
            },
            {
                "dioula": "Muso",
                "french": "Femme / Épouse",
                "context": "Genre féminin ou épouse",
                "phonetic": "mou-so",
            },
            {
                "dioula": "Tɔmɔgɔ",
                "french": "Ami(e) / Camarade",
                "context": "Personne proche, ami de confiance",
                "phonetic": "tɔ-mɔ-gɔ",
            },
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "Comment dit-on 'Mère' en Dioula ?",
                "options": ["Fa", "Nba", "Den", "Kɔrɔ"],
                "correct": 1,
                "explanation": "'Nba' désigne la mère en Dioula. La mère est une figure centrale dans la culture ivoirienne.",
            },
            {
                "id": "q2",
                "question": "Que signifie 'Dɔgɔ' ?",
                "options": ["Grand frère / Sœur aînée", "Père", "Petit frère / Petite sœur", "Enfant"],
                "correct": 2,
                "explanation": "'Dɔgɔ' désigne le cadet — le petit frère ou la petite sœur.",
            },
            {
                "id": "q3",
                "question": "Comment dit-on 'Père' en Dioula ?",
                "options": ["Nba", "Fa", "Ke", "Den"],
                "correct": 1,
                "explanation": "'Fa' est le mot Dioula pour désigner le père.",
            },
            {
                "id": "q4",
                "question": "Quel mot désigne l'aîné(e) dans une famille ?",
                "options": ["Dɔgɔ", "Den", "Kɔrɔ", "Muso"],
                "correct": 2,
                "explanation": "'Kɔrɔ' désigne l'aîné(e) — grand frère ou grande sœur. C'est une figure de respect.",
            },
            {
                "id": "q5",
                "question": "Comment dit-on 'Enfant' en Dioula ?",
                "options": ["Muso", "Ke", "Tɔmɔgɔ", "Den"],
                "correct": 3,
                "explanation": "'Den' désigne tout enfant en Dioula, garçon ou fille.",
            },
        ],
    },

    # ── Leçon 3 : Se Présenter ───────────────────────────────
    {
        "id": 3,
        "title": "Se Présenter",
        "theme": "introductions",
        "emoji": "🤝",
        "description": "Comment se présenter et faire connaissance en Dioula",
        "content": [
            {
                "dioula": "N togo ye...",
                "french": "Je m'appelle...",
                "context": "Pour dire son prénom — suivi directement du prénom",
                "phonetic": "n to-go yé",
            },
            {
                "dioula": "I togo ye di?",
                "french": "Comment tu t'appelles ?",
                "context": "Demander le prénom de quelqu'un",
                "phonetic": "i to-go yé di",
            },
            {
                "dioula": "N baro",
                "french": "Mon ami / Mon frère",
                "context": "Terme d'affection entre amis — très courant",
                "phonetic": "n ba-ro",
            },
            {
                "dioula": "N ye ivoirien ye",
                "french": "Je suis ivoirien(ne)",
                "context": "Exprimer sa nationalité",
                "phonetic": "n yé ivoirien yé",
            },
            {
                "dioula": "N bɛ Abidjan",
                "french": "Je suis à Abidjan",
                "context": "Dire où on habite ou où on se trouve",
                "phonetic": "n bè Abidjan",
            },
            {
                "dioula": "N bɛ baara kɛ",
                "french": "Je travaille",
                "context": "Parler de son activité professionnelle",
                "phonetic": "n bè ba-ra ké",
            },
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "Comment demande-t-on le prénom de quelqu'un en Dioula ?",
                "options": ["N togo ye", "I togo ye di?", "N be di", "Fo!"],
                "correct": 1,
                "explanation": "'I togo ye di?' signifie littéralement 'Ton nom est quoi?' en Dioula.",
            },
            {
                "id": "q2",
                "question": "Comment dit-on 'Je m'appelle...' en Dioula ?",
                "options": ["I togo ye di?", "N baro", "N togo ye...", "N be di"],
                "correct": 2,
                "explanation": "'N togo ye...' suivi du prénom signifie 'Je m'appelle...'. Ex: 'N togo ye Kofi'.",
            },
            {
                "id": "q3",
                "question": "Que signifie 'N baro' ?",
                "options": ["Je travaille", "Mon ami / Mon frère", "Je suis ivoirien", "Je vais bien"],
                "correct": 1,
                "explanation": "'N baro' est un terme affectueux très courant entre amis en Côte d'Ivoire.",
            },
        ],
    },

    # ── Leçon 4 : Le Marché ──────────────────────────────────
    {
        "id": 4,
        "title": "Le Marché",
        "theme": "market",
        "emoji": "🛒",
        "description": "Vocabulaire essentiel pour faire ses achats au marché ivoirien",
        "content": [
            {
                "dioula": "Ne bɛ taa sugu la",
                "french": "Je vais au marché",
                "context": "Phrase du quotidien très utilisée",
                "phonetic": "né bè ta sou-gou la",
            },
            {
                "dioula": "Juru",
                "french": "Argent",
                "context": "L'argent en général",
                "phonetic": "djou-rou",
            },
            {
                "dioula": "Sɔrɔ",
                "french": "Acheter / Obtenir",
                "context": "Action d'acheter quelque chose",
                "phonetic": "sɔ-rɔ",
            },
            {
                "dioula": "Feere",
                "french": "Vendre",
                "context": "Action de vendre",
                "phonetic": "fé-ré",
            },
            {
                "dioula": "A jaabi di?",
                "french": "Quel est le prix ?",
                "context": "Pour négocier — très important au marché !",
                "phonetic": "a dja-bi di",
            },
            {
                "dioula": "A man di",
                "french": "Ce n'est pas bon / Trop cher",
                "context": "Pour négocier à la baisse",
                "phonetic": "a man di",
            },
            {
                "dioula": "A ye di",
                "french": "C'est bien / C'est bon",
                "context": "Approuver le prix ou la qualité",
                "phonetic": "a yé di",
            },
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "Comment dit-on 'Je vais au marché' en Dioula ?",
                "options": ["N bɛ sɔrɔ", "Ne bɛ taa sugu la", "A ye feere", "Juru di"],
                "correct": 1,
                "explanation": "'Ne bɛ taa sugu la' — 'sugu' signifie marché en Dioula.",
            },
            {
                "id": "q2",
                "question": "Comment dit-on 'Argent' en Dioula ?",
                "options": ["Sugu", "Feere", "Juru", "Sɔrɔ"],
                "correct": 2,
                "explanation": "'Juru' signifie argent. Très utile au marché !",
            },
            {
                "id": "q3",
                "question": "Que dit-on pour demander le prix d'un article ?",
                "options": ["A ye di", "Ne bɛ taa", "A jaabi di?", "Juru"],
                "correct": 2,
                "explanation": "'A jaabi di?' signifie 'Quel est le prix?' — phrase essentielle pour négocier.",
            },
            {
                "id": "q4",
                "question": "Comment exprimer son accord sur un prix ?",
                "options": ["A man di", "A ye di", "Jɔ!", "Taa!"],
                "correct": 1,
                "explanation": "'A ye di' signifie 'c'est bien/c'est bon' — pour accepter un prix ou approuver.",
            },
        ],
    },

    # ── Leçon 5 : La Nourriture ──────────────────────────────
    {
        "id": 5,
        "title": "La Nourriture",
        "theme": "food",
        "emoji": "🍽️",
        "description": "La gastronomie ivoirienne et les repas du quotidien en Dioula",
        "content": [
            {
                "dioula": "Dumu",
                "french": "Manger / Nourriture",
                "context": "Verbe manger ou nom nourriture selon le contexte",
                "phonetic": "dou-mou",
            },
            {
                "dioula": "Min",
                "french": "Boire",
                "context": "Le verbe boire",
                "phonetic": "min",
            },
            {
                "dioula": "Ji",
                "french": "Eau",
                "context": "L'eau — ressource essentielle",
                "phonetic": "dji",
            },
            {
                "dioula": "Tiga",
                "french": "Arachide",
                "context": "Ingrédient clé de la cuisine ivoirienne (sauce tigadèguè)",
                "phonetic": "ti-ga",
            },
            {
                "dioula": "Malo",
                "french": "Riz",
                "context": "Aliment de base en Côte d'Ivoire",
                "phonetic": "ma-lo",
            },
            {
                "dioula": "N be kɔngɔ",
                "french": "J'ai faim",
                "context": "Exprimer la faim",
                "phonetic": "n bé kɔn-gɔ",
            },
            {
                "dioula": "N be ministerege",
                "french": "J'ai soif",
                "context": "Exprimer la soif",
                "phonetic": "n bé mi-nis-tè-rè-gué",
            },
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "Comment dit-on 'Eau' en Dioula ?",
                "options": ["Malo", "Ji", "Tiga", "Dumu"],
                "correct": 1,
                "explanation": "'Ji' signifie eau en Dioula. Essentiel pour survivre sous le soleil d'Abidjan !",
            },
            {
                "id": "q2",
                "question": "Quel mot désigne le riz en Dioula ?",
                "options": ["Tiga", "Dumu", "Malo", "Min"],
                "correct": 2,
                "explanation": "'Malo' signifie riz — l'aliment de base en Côte d'Ivoire.",
            },
            {
                "id": "q3",
                "question": "Comment dit-on 'J'ai faim' en Dioula ?",
                "options": ["N be ministerege", "N be kɔngɔ", "N be di", "N be dumu"],
                "correct": 1,
                "explanation": "'N be kɔngɔ' exprime la faim. 'Kɔngɔ' signifie la faim.",
            },
        ],
    },

    # ── Leçon 6 : Les Chiffres ───────────────────────────────
    {
        "id": 6,
        "title": "Les Chiffres",
        "theme": "numbers",
        "emoji": "🔢",
        "description": "Compter en Dioula — utile au marché et dans la vie quotidienne",
        "content": [
            {"dioula": "Kelen", "french": "1 — Un",      "context": "Premier chiffre", "phonetic": "ké-len"},
            {"dioula": "Fila",  "french": "2 — Deux",    "context": "Deuxième",         "phonetic": "fi-la"},
            {"dioula": "Saba",  "french": "3 — Trois",   "context": "Troisième",        "phonetic": "sa-ba"},
            {"dioula": "Naani", "french": "4 — Quatre",  "context": "Quatrième",        "phonetic": "na-ni"},
            {"dioula": "Duuru", "french": "5 — Cinq",    "context": "Cinquième",        "phonetic": "dou-rou"},
            {"dioula": "Wɔɔrɔ", "french": "6 — Six",    "context": "Sixième",          "phonetic": "wɔ-rɔ"},
            {"dioula": "Wolonwula", "french": "7 — Sept","context": "Septième",         "phonetic": "wo-lon-ou-la"},
            {"dioula": "Segin", "french": "8 — Huit",    "context": "Huitième",         "phonetic": "sé-gin"},
            {"dioula": "Kɔnɔntɔn", "french": "9 — Neuf","context": "Neuvième",         "phonetic": "kɔ-nɔn-tɔn"},
            {"dioula": "Tan",   "french": "10 — Dix",    "context": "Dixième",          "phonetic": "tan"},
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "Comment dit-on '3' en Dioula ?",
                "options": ["Fila", "Kelen", "Saba", "Naani"],
                "correct": 2,
                "explanation": "'Saba' signifie trois en Dioula.",
            },
            {
                "id": "q2",
                "question": "Quel chiffre est 'Tan' en Dioula ?",
                "options": ["5", "7", "10", "8"],
                "correct": 2,
                "explanation": "'Tan' signifie dix (10) en Dioula.",
            },
            {
                "id": "q3",
                "question": "Comment dit-on '2' en Dioula ?",
                "options": ["Kelen", "Fila", "Saba", "Duuru"],
                "correct": 1,
                "explanation": "'Fila' signifie deux (2) en Dioula.",
            },
            {
                "id": "q4",
                "question": "Quel chiffre est 'Duuru' ?",
                "options": ["4", "5", "6", "7"],
                "correct": 1,
                "explanation": "'Duuru' signifie cinq (5) en Dioula.",
            },
        ],
    },
]

# ── Catalogue phrases audio pour Niveau 2 ────────────────────
NIVEAU2_AUDIO_PHRASES = [
    {"id": 1,  "dioula": "I ni ce",             "french": "Bonjour",              "category": "salutations"},
    {"id": 2,  "dioula": "I ni sogoma",          "french": "Bonjour (matin)",      "category": "salutations"},
    {"id": 3,  "dioula": "I be di wa?",          "french": "Comment tu vas?",      "category": "salutations"},
    {"id": 4,  "dioula": "N be di",              "french": "Je vais bien",         "category": "salutations"},
    {"id": 5,  "dioula": "N togo ye Kofi",       "french": "Je m'appelle Kofi",    "category": "presentations"},
    {"id": 6,  "dioula": "Ne bɛ taa sugu la",   "french": "Je vais au marché",    "category": "vie_quotidienne"},
    {"id": 7,  "dioula": "A ye di",              "french": "C'est bien / C'est bon","category": "expressions"},
    {"id": 8,  "dioula": "I ni baara",           "french": "Bravo pour ton travail","category": "expressions"},
    {"id": 9,  "dioula": "N be kɔngɔ",          "french": "J'ai faim",            "category": "vie_quotidienne"},
    {"id": 10, "dioula": "A jaabi di?",          "french": "Quel est le prix?",    "category": "marche"},
    {"id": 11, "dioula": "Kelen, Fila, Saba",   "french": "Un, Deux, Trois",      "category": "nombres"},
    {"id": 12, "dioula": "I ni wula",            "french": "Bonsoir",              "category": "salutations"},
]