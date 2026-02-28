# app/services/rag_service.py  —  VERSION GEMINI 2.5 (Hackathon)
import os
import time
from typing import List, Dict
from difflib import SequenceMatcher
from pathlib import Path

# ── Prompt optimisé (validé en benchmark Colab) ──────────────
DIOULA_PROMPT = """Tu es Mariam, un professeur bienveillant et expert en langue \
Dioula (Dyula) de Côte d'Ivoire. Tu aides les apprenants à comprendre et pratiquer le Dioula.

Voici des phrases Dioula de référence tirées du corpus Koumankan :
{context}

Règles impératives :
1. Réponds TOUJOURS en incluant la phrase Dioula ET sa traduction française
2. Si l'apprenant fait une erreur, corrige-le avec bienveillance
3. Cite des exemples concrets du corpus fourni ci-dessus
4. Sois chaleureux, pédagogue et encourageant
5. Format :
   🗣️ En Dioula : [phrase]
   🇫🇷 En Français : [traduction]
   💡 Conseil : [astuce courte]

Question ou phrase de l'apprenant : {question}"""

# Chemin vers la base ChromaDB pré-construite (importée depuis Colab)
CHROMA_DB_DIR = Path(__file__).parent / "dioula_chroma_db"


class DioulaRAGService:
    def __init__(self):
        self.vectorstore = None
        self.llm = None
        self.chain = None
        self._initialized = False
        self._fallback_pairs: List[Dict] = []

    # ── Initialisation (appelée au démarrage via lifespan) ────
    def initialize(self):
        if self._initialized:
            return
        print("[INIT] Initialisation du RAG Dioula avec Google Gemini...")

        # Charger les paires de fallback depuis le dataset
        from app.data.loader import load_dioula_pairs
        # Mode test: 50 phrases pour construction rapide
        self._fallback_pairs = load_dioula_pairs(max_samples=50)

        try:
            from app.config import LLM_PROVIDER, GOOGLE_API_KEY, MISTRAL_API_KEY, LLM_TEMPERATURE, LLM_MAX_TOKENS, GEMINI_LLM_MODEL, GEMINI_EMBED_MODEL, MISTRAL_MODEL
            from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
            from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
            from langchain_community.vectorstores import Chroma
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_core.output_parsers import StrOutputParser
            from langchain_core.documents import Document
            from pydantic import SecretStr

            # 1. Sélection du provider
            provider = LLM_PROVIDER
            if not GOOGLE_API_KEY and MISTRAL_API_KEY:
                provider = "mistral"
            elif GOOGLE_API_KEY and not MISTRAL_API_KEY:
                provider = "gemini"

            print(f"[INIT] Utilisation du provider: {provider}")

            # 2. Embeddings
            if provider == "mistral" and MISTRAL_API_KEY:
                embeddings = MistralAIEmbeddings(
                    model="mistral-embed",
                    api_key=SecretStr(MISTRAL_API_KEY),
                )
                collect_name = "dioula_corpus_mistral"
                p_dir = str(CHROMA_DB_DIR / "mistral_built")
            else:
                embeddings = GoogleGenerativeAIEmbeddings(
                    model=GEMINI_EMBED_MODEL,
                    google_api_key=GOOGLE_API_KEY,
                )
                collect_name = "dioula_corpus_gemini"
                p_dir = str(CHROMA_DB_DIR / "gemini_built")

            # 3. ChromaDB
            documents = [
                Document(
                    page_content=f"Dioula: {p['dioula']}\nFrançais: {p['french']}",
                    metadata={"id": p["id"], "dioula": p["dioula"], "french": p["french"]},
                )
                for p in self._fallback_pairs
            ]

            if Path(p_dir).exists():
                self.vectorstore = Chroma(
                    persist_directory=p_dir,
                    embedding_function=embeddings,
                )
                print(f"[OK] ChromaDB chargée depuis cache")
            else:
                print(f"[BUILD] Construction ChromaDB...")
                self.vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=embeddings,
                    collection_name=collect_name,
                    persist_directory=p_dir,
                )

            # 4. LLM
            if provider == "mistral":
                self.llm = ChatMistralAI(
                    api_key=SecretStr(MISTRAL_API_KEY),
                    model=MISTRAL_MODEL,
                    temperature=LLM_TEMPERATURE,
                    max_tokens=LLM_MAX_TOKENS,
                )
            else:
                self.llm = ChatGoogleGenerativeAI(
                    model=GEMINI_LLM_MODEL,
                    google_api_key=GOOGLE_API_KEY,
                    temperature=LLM_TEMPERATURE,
                    max_tokens=LLM_MAX_TOKENS,
                )

            # 4. Chaîne LCEL (RAG)
            prompt = ChatPromptTemplate.from_template(DIOULA_PROMPT)
            assert self.vectorstore is not None
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

            def format_docs(docs):
                return "\n\n".join(d.page_content for d in docs)

            self.chain = (
                {"context": retriever | format_docs, "question": lambda x: x}
                | prompt
                | self.llm
                | StrOutputParser()
            )

            self._initialized = True
            print(f"[OK] RAG Gemini prêt !")

        except Exception as e:
            print(f"[WARN] RAG Gemini non disponible ({e}) -> mode fallback")
            self._initialized = True

    # ── Requête IA (utilisée par tous les niveaux) ────────────
    def query(self, question: str) -> str:
        if not self._initialized:
            self.initialize()
        if self.chain:
            for attempt in range(3):
                try:
                    return self.chain.invoke(question)
                except Exception as e:
                    err_str = str(e)
                    if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                        wait = 50 * (attempt + 1)
                        print(f"⏳ Rate limit LLM — retry dans {wait}s...")
                        time.sleep(wait)
                    else:
                        print(f"Erreur RAG query : {e}")
                        break
        # Fallback textuel
        similar = self.search_similar(question, k=3)
        if similar:
            examples = "\n".join(
                [f"  • {p['dioula']}  =  {p['french']}" for p in similar]
            )
            return f"🗣️ Phrases Dioula proches :\n{examples}\n\n💡 I ni baara ! 🌍"
        return "I ni ce ! Pose-moi une question sur le Dioula 😊"

    # ── Recherche sémantique ──────────────────────────────────
    def search_similar(self, text: str, k: int = 3) -> List[Dict]:
        if not self._initialized:
            self.initialize()
        if self.vectorstore:
            try:
                docs = self.vectorstore.similarity_search(text, k=k)
                return [
                    {"dioula": d.metadata["dioula"], "french": d.metadata["french"]}
                    for d in docs
                ]
            except Exception:
                pass
        # Fallback SequenceMatcher
        text_lower = text.lower()
        scored = sorted(
            self._fallback_pairs,
            key=lambda p: max(
                SequenceMatcher(None, text_lower, p["dioula"].lower()).ratio(),
                SequenceMatcher(None, text_lower, p["french"].lower()).ratio(),
            ),
            reverse=True,
        )
        return scored[:k]

    # ── Évaluation prononciation Dioula ───────────────────────
    def evaluate_dioula(self, user_input: str, expected: str) -> Dict:
        if not self._initialized:
            self.initialize()
        similarity = SequenceMatcher(
            None, user_input.lower().strip(), expected.lower().strip()
        ).ratio()
        score = round(similarity * 10, 1)
        correct = similarity > 0.7
        feedback = self.query(
            f"L'apprenant a écrit : '{user_input}'. "
            f"La bonne réponse était : '{expected}'. "
            f"Score : {score}/10. Donne un retour encourageant avec la correction."
        )
        return {"score": score, "correct": correct, "feedback": feedback}

    # ── Explication détaillée d'une phrase ─────────────────────
    def explain_phrase(self, dioula: str, french: str) -> str:
        return self.query(
            f"Explique la phrase Dioula '{dioula}' qui signifie '{french}'. "
            f"Donne : 1) le contexte d'utilisation, "
            f"2) une variante possible, "
            f"3) une phrase d'exemple complète avec traduction."
        )

    # ── Génération dynamique de quiz ──────────────────────────
    def generate_quiz_question(self, lesson_content: List[Dict]) -> Dict:
        if not self.chain:
            return {}
        examples = "\n".join(
            [f"- {p['dioula']} = {p['french']}" for p in lesson_content[:5]]
        )
        raw = self.query(
            f"À partir de ces phrases Dioula :\n{examples}\n\n"
            f"Génère UNE question de quiz en JSON strict :\n"
            f'{{"question":"...","options":["A","B","C","D"],"correct":0,"explanation":"..."}}\n'
            f"Réponds UNIQUEMENT avec le JSON, rien d'autre."
        )
        try:
            import json
            start, end = raw.find("{"), raw.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(raw[start:end])
        except Exception as e:
            print(f"Erreur génération quiz dynamique: {e}")
        return {}


# ── Singleton utilisé par tous les routers ────────────────────
rag_service = DioulaRAGService()