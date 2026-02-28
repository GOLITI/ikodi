"""
GriotKnowledge — orchestrator.py
===================================
Microservice d'orchestration LLM.

Responsabilités :
    1. Recevoir la question + les documents récupérés par le Retriever
    2. Construire un prompt contextualisé (RAG)
    3. Appeler le LLM (Mistral via HuggingFace ou fallback local)
    4. Retourner une ReponseGriot structurée
"""

import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.models import RequeteUtilisateur, ResultatRecherche, ReponseGriot, Langue
from app.retriever import Retriever

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "mistralai/mistral-7b-instruct")


# ─────────────────────────────────────────────────────────────
# PROMPT TEMPLATE
# ─────────────────────────────────────────────────────────────

PROMPT_GRIOT = PromptTemplate(
    input_variables=["question", "contexte", "nb_sources"],
    template="""Tu es GriotKnowledge, un assistant culturel expert en sagesse ivoirienne.
Tu puises uniquement dans les contes, proverbes et légendes des peuples de Côte d'Ivoire.

RÈGLES ABSOLUES :
- Réponds UNIQUEMENT en te basant sur les sources fournies ci-dessous.
- Ne fabrique aucune histoire ou proverbe de ton propre chef.
- Cite toujours le titre de la source dont tu t'inspires.
- Si les sources ne permettent pas de répondre, dis-le honnêtement.
- Réponds en français, avec bienveillance et respect des traditions.

SOURCES CULTURELLES DISPONIBLES ({nb_sources} document(s)) :
─────────────────────────────────────────────────────
{contexte}
─────────────────────────────────────────────────────

QUESTION : {question}

RÉPONSE (en t'appuyant sur les sources ci-dessus) :""",
)


# ─────────────────────────────────────────────────────────────
# FALLBACK LLM  (mode sans token ou si HF indisponible)
# ─────────────────────────────────────────────────────────────

class FallbackLLM:
    """
    Synthétise une réponse directement depuis les sources
    sans appel API externe. Utile pour démos offline.
    """

    def invoke(self, inputs) -> str:
        import re
        
        # Si inputs est un dict, formater le prompt
        if isinstance(inputs, dict):
            texte = PROMPT_GRIOT.format(**inputs)
        else:
            texte = str(inputs)
        
        sources = re.findall(r'\[Source \d+\](.*?)(?=\[Source|\Z)', texte, re.DOTALL)

        if not sources:
            return "La sagesse ivoirienne nous enseigne que chaque situation mérite réflexion."

        lignes = ["La sagesse des peuples de Côte d'Ivoire nous éclaire ainsi :\n"]
        for source in sources[:3]:
            titre_m = re.search(r'(.+?)\(', source.strip())
            ens_m   = re.search(r"Enseignement\s*:\s*(.+)", source)
            if titre_m:
                lignes.append(f"• {titre_m.group(1).strip()} :")
            if ens_m:
                lignes.append(f"  \"{ens_m.group(1).strip()}\"")
            else:
                contenu = re.sub(r'\n+', ' ', source.strip())
                lignes.append(f"  {contenu[:150].strip()}...")
            lignes.append("")

        lignes.append(
            "Ces enseignements ancestraux offrent des réponses intemporelles "
            "aux questions de la vie."
        )
        return "\n".join(lignes)


# ─────────────────────────────────────────────────────────────
# ORCHESTRATOR
# ─────────────────────────────────────────────────────────────

class Orchestrator:
    """
    Orchestre le pipeline RAG complet :
    Question → Retriever → LLM → ReponseGriot
    """

    def __init__(self):
        self.retriever = Retriever()
        self.llm       = self._charger_llm()
        
        # Créer la chaîne selon le type de LLM
        if isinstance(self.llm, FallbackLLM):
            self.chain = self.llm  # FallbackLLM gère déjà la chaîne
        else:
            self.chain = PROMPT_GRIOT | self.llm | StrOutputParser()
        
        print("✅ Orchestrator prêt")

    # ── Chargement du LLM ────────────────────────────────────

    def _charger_llm(self):
        """
        Tente de charger :
          1. OpenRouter (si OPENROUTER_API_KEY défini)
          2. FallbackLLM local si indisponible
        """
        if not OPENROUTER_API_KEY:
            print("⚠️  Pas de OPENROUTER_API_KEY — FallbackLLM activé")
            return FallbackLLM()

        try:
            from langchain_openai import ChatOpenAI
            
            print(f"⏳ Connexion OpenRouter : {LLM_MODEL}")
            
            llm = ChatOpenAI(
                model=LLM_MODEL,
                openai_api_key=OPENROUTER_API_KEY,
                openai_api_base="https://openrouter.ai/api/v1",
                temperature=0.3,
                max_tokens=512,
            )
            
            print(f"✅ LLM connecté : {LLM_MODEL} (OpenRouter)")
            return llm

        except Exception as e:
            print(f"⚠️  OpenRouter échoué : {type(e).__name__}")
            print("   → Bascule sur FallbackLLM")
            return FallbackLLM()

    # ── Construction du contexte ─────────────────────────────

    def _construire_contexte(self, resultats: list[ResultatRecherche]) -> str:
        """Formate les documents récupérés en bloc lisible par le LLM."""
        blocs = []
        for i, r in enumerate(resultats, 1):
            bloc = (
                f"[Source {i}] {r.titre_parent} "
                f"({r.type_contenu.value} — peuple {r.ethnie.value})\n"
                f"{r.contenu}"
            )
            if r.morale:
                bloc += f"\nEnseignement : {r.morale}"
            blocs.append(bloc)
        return "\n\n".join(blocs)

    # ── Méthode principale ───────────────────────────────────

    def repondre(
        self,
        requete: RequeteUtilisateur,
        resultats: list[ResultatRecherche] | None = None,
    ) -> ReponseGriot:
        """Pipeline RAG complet : Question → Sources → LLM → ReponseGriot."""

        if resultats is None:
            resultats = self.retriever.rechercher_depuis_requete(requete)

        if not resultats:
            return ReponseGriot(
                question=requete.question,
                reponse=(
                    "Je n'ai pas trouvé de sagesse ivoirienne correspondant "
                    "à votre question dans le corpus actuel."
                ),
                sources=[],
                nb_sources=0,
                langue_reponse=requete.langue_reponse,
            )

        contexte = self._construire_contexte(resultats)

        try:
            reponse_texte = self.chain.invoke({
                "question":   requete.question,
                "contexte":   contexte,
                "nb_sources": len(resultats),
            })
            reponse_texte = reponse_texte.strip()
        except Exception as e:
            print(f"❌ Erreur détaillée: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            reponse_texte = (
                "Une erreur est survenue lors de la génération de la réponse. "
                "Veuillez consulter les sources ci-dessous pour obtenir la sagesse demandée."
            )

        return ReponseGriot(
            question=requete.question,
            reponse=reponse_texte,
            sources=resultats,
            nb_sources=len(resultats),
            langue_reponse=requete.langue_reponse,
        )

    def repondre_depuis_question(self, question: str, nb_resultats: int = 3) -> ReponseGriot:
        """Raccourci pour poser une question simple en string."""
        requete = RequeteUtilisateur(question=question, nb_resultats=nb_resultats)
        return self.repondre(requete)


# ─────────────────────────────────────────────────────────────
# TEST  (python app/orchestrator.py)
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from rich.console import Console
    from rich.panel import Panel
    from rich.rule import Rule

    console = Console()
    console.print("\n[bold yellow]Test Orchestrator GriotKnowledge[/bold yellow]\n")

    orchestrator = Orchestrator()

    questions = [
        "Comment gérer un conflit avec mon voisin selon la sagesse ivoirienne ?",
        "Je me sens découragé face aux obstacles. Que dit la tradition ?",
        "Quelle est l'importance de l'unité dans la culture ivoirienne ?",
    ]

    for question in questions:
        console.print(Rule(f"[cyan]{question}[/cyan]"))
        reponse = orchestrator.repondre_depuis_question(question, nb_resultats=2)

        console.print(Panel(
            reponse.reponse,
            title="🗣️  GriotKnowledge répond",
            border_style="yellow",
            padding=(1, 2),
        ))

        console.print(f"[dim]Sources ({reponse.nb_sources}) :[/dim]")
        for s in reponse.sources:
            console.print(f"  [dim]• {s.titre_parent} [{s.ethnie.value}] score={s.score}[/dim]")
        console.print()