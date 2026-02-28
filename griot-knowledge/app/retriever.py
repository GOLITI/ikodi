"""
GriotKnowledge — retriever.py
===============================
Microservice de recherche sémantique.

Responsabilités :
    1. Transformer la question de l'utilisateur en vecteur
    2. Rechercher les chunks les plus proches dans Qdrant
    3. Appliquer des filtres optionnels (ethnie, type de contenu)
    4. Retourner les résultats classés par score de similarité

Utilisation :
    retriever = Retriever()
    resultats = retriever.rechercher("Comment gérer un conflit ?")
"""

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
# sentence_transformers is optional in the lightweight Docker image.
# Import lazily in __init__ to allow starting the service without heavy ML deps.

try:
    from .models import (
        RequeteUtilisateur,
        ResultatRecherche,
        TypeContenu,
        Ethnie,
        Langue,
    )
except ImportError:
    from models import (
        RequeteUtilisateur,
        ResultatRecherche,
        TypeContenu,
        Ethnie,
        Langue,
    )

load_dotenv()

QDRANT_HOST     = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT     = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "griot_corpus")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Score minimum pour qu'un résultat soit considéré pertinent
SCORE_MINIMUM = 0.15


# ─────────────────────────────────────────────────────────────
# RETRIEVER
# ─────────────────────────────────────────────────────────────

class Retriever:
    """
    Recherche les documents culturels les plus pertinents
    par rapport à une question utilisateur.
    """

    def __init__(self):
        print(f"⏳ Chargement embedding : {EMBEDDING_MODEL}")
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            print("✅ SentenceTransformer chargé")
        except Exception:
            self.model = None
            print("⚠️  sentence-transformers non installé — mode fallback (pas d'embeddings)")
        try:
            self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
            print("✅ Retriever connecté à Qdrant")
        except Exception as e:
            self.client = None
            print(f"⚠️  Qdrant non disponible ({QDRANT_HOST}:{QDRANT_PORT}) — mode fallback activé: {e}")

        print("✅ Retriever prêt (mode dégradé si nécessaire)")

    # ── Vectorisation de la requête ──────────────────────────

    def _vectoriser_requete(self, question: str) -> list[float]:
        """Transforme la question en vecteur numérique."""
        if self.model is None:
            raise RuntimeError(
                "Embeddings model not available in this container. "
                "Install 'sentence-transformers' or provide a running embedding service."
            )
        vecteur = self.model.encode(question, normalize_embeddings=True)
        return vecteur.tolist()

    # ── Construction du filtre Qdrant ────────────────────────

    def _construire_filtre(
        self,
        filtre_ethnie: Ethnie | None,
        filtre_type: TypeContenu | None,
    ) -> Filter | None:
        """
        Construit un filtre Qdrant selon les critères optionnels.
        Si aucun filtre, retourne None (recherche globale).
        """
        conditions = []

        if filtre_ethnie:
            conditions.append(
                FieldCondition(
                    key="ethnie",
                    match=MatchValue(value=filtre_ethnie.value)
                )
            )

        if filtre_type:
            conditions.append(
                FieldCondition(
                    key="type_contenu",
                    match=MatchValue(value=filtre_type.value)
                )
            )

        if not conditions:
            return None

        return Filter(must=conditions)

    # ── Dédoublonnage ────────────────────────────────────────

    def _dedoublonner(self, resultats: list[ResultatRecherche]) -> list[ResultatRecherche]:
        """
        Évite de retourner plusieurs chunks du même document.
        Garde uniquement le chunk avec le meilleur score par doc_id.
        """
        vus: dict[str, ResultatRecherche] = {}
        for r in resultats:
            if r.doc_id not in vus or r.score > vus[r.doc_id].score:
                vus[r.doc_id] = r
        # Retrier par score décroissant
        return sorted(vus.values(), key=lambda x: x.score, reverse=True)

    # ── Méthode principale ───────────────────────────────────

    def rechercher(
        self,
        question: str,
        nb_resultats: int = 3,
        filtre_ethnie: Ethnie | None = None,
        filtre_type: TypeContenu | None = None,
        dedoublonner: bool = True,
    ) -> list[ResultatRecherche]:
        """
        Recherche les documents les plus pertinents pour une question.

        Args:
            question      : La question ou situation de l'utilisateur
            nb_resultats  : Nombre de résultats souhaités (après dédoublonnage)
            filtre_ethnie : Filtrer sur une ethnie spécifique
            filtre_type   : Filtrer sur conte, proverbe, etc.
            dedoublonner  : Ne garder qu'un chunk par document source

        Returns:
            Liste de ResultatRecherche triés par pertinence décroissante
        """
        # On cherche plus de candidats pour compenser le dédoublonnage
        limite_recherche = nb_resultats * 4 if dedoublonner else nb_resultats

        # If embeddings model is not available, use a lightweight textual
        # fallback that searches the corpus JSON files for matching text.
        if self.model is None:
            return self._fallback_search(question, nb_resultats, filtre_ethnie, filtre_type)

        # 1. Vectoriser la question
        if self.client is None:
            print("⚠️  Qdrant indisponible — utilisation du fallback textuel")
            return self._fallback_search(question, nb_resultats, filtre_ethnie, filtre_type)

        vecteur_question = self._vectoriser_requete(question)

        # 2. Construire le filtre
        filtre = self._construire_filtre(filtre_ethnie, filtre_type)

        # 3. Recherche dans Qdrant
        hits = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=vecteur_question,
            limit=limite_recherche,
            query_filter=filtre,
            score_threshold=SCORE_MINIMUM,
            with_payload=True,
        ).points

        # 4. Convertir en ResultatRecherche
        resultats = []
        for hit in hits:
            p = hit.payload
            try:
                r = ResultatRecherche(
                    chunk_id=p.get("chunk_id", ""),
                    doc_id=p.get("doc_id", ""),
                    contenu=p.get("contenu", ""),
                    titre_parent=p.get("titre_parent", ""),
                    ethnie=Ethnie(p.get("ethnie", "autre")),
                    type_contenu=TypeContenu(p.get("type_contenu", "conte")),
                    morale=p.get("morale"),
                    score=round(hit.score, 4),
                )
                resultats.append(r)
            except Exception as e:
                print(f"⚠️  Erreur parsing résultat {hit.id} : {e}")

        # 5. Dédoublonner si demandé
        if dedoublonner:
            resultats = self._dedoublonner(resultats)

        # 6. Limiter au nombre demandé
        return resultats[:nb_resultats]

    def rechercher_depuis_requete(self, requete: RequeteUtilisateur) -> list[ResultatRecherche]:
        """Surcharge pratique qui accepte directement un objet RequeteUtilisateur."""
        return self.rechercher(
            question=requete.question,
            nb_resultats=requete.nb_resultats,
            filtre_ethnie=requete.filtre_ethnie,
            filtre_type=requete.filtre_type,
        )

    # ── Fallback text search (no embeddings) ──────────────────────────
    def _fallback_search(
        self,
        question: str,
        nb_resultats: int = 3,
        filtre_ethnie: Ethnie | None = None,
        filtre_type: TypeContenu | None = None,
    ) -> list[ResultatRecherche]:
        """Recherche basique par présence de mots-clés dans les fichiers JSON
        du dossier `data/corpus`. Retourne des `ResultatRecherche` avec scores
        heuristiques (nombre de termes en commun).
        """
        import json
        import glob
        from pathlib import Path

        corpus_dir = Path(__file__).resolve().parents[1] / 'data' / 'corpus'
        files = glob.glob(str(corpus_dir / '*.json'))
        tokens = [t.lower() for t in question.split() if len(t) > 2]

        candidates = []
        for f in files:
            try:
                with open(f, 'r', encoding='utf-8') as fh:
                    items = json.load(fh)
            except Exception:
                continue

            for it in items:
                # Apply simple filters
                if filtre_ethnie and it.get('ethnie') != filtre_ethnie.value:
                    continue
                if filtre_type and it.get('type_contenu') != filtre_type.value:
                    continue

                texte = ' '.join([str(it.get('titre','')), str(it.get('contenu',''))]).lower()
                match_count = sum(1 for tok in tokens if tok in texte)
                if match_count == 0:
                    continue

                # Heuristic score: normalized by number of tokens
                score = match_count / max(1, len(tokens))

                from app.models import ResultatRecherche

                r = ResultatRecherche(
                    chunk_id=it.get('id',''),
                    doc_id=it.get('id',''),
                    contenu=it.get('contenu',''),
                    titre_parent=it.get('titre',''),
                    ethnie=Ethnie(it.get('ethnie','autre')),
                    type_contenu=TypeContenu(it.get('type_contenu','conte')),
                    morale=it.get('morale'),
                    score=round(float(score), 4),
                )
                candidates.append(r)

        # Sort by score desc and deduplicate by doc_id
        candidates = sorted(candidates, key=lambda x: x.score, reverse=True)
        if not candidates:
            return []

        # Keep top nb_resultats
        return candidates[:nb_resultats]


# ─────────────────────────────────────────────────────────────
# TEST RAPIDE  (python app/retriever.py)
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from rich.console import Console
    from rich.table import Table
    from rich import box

    console = Console()

    console.print("\n[bold yellow]🥁 Test du Retriever GriotKnowledge[/bold yellow]\n")

    r = Retriever()

    # Jeu de questions de test
    questions = [
        ("Comment gérer un conflit entre voisins ?",         None,             None),
        ("Je veux réussir malgré les obstacles.",            None,             None),
        ("Sagesse sur la parole et la communication",        None,             TypeContenu.PROVERBE),
        ("Histoire sur la nature et la gratitude",           Ethnie.BAOULE,    TypeContenu.CONTE),
        ("L'importance de travailler ensemble en équipe",    None,             None),
    ]

    for question, ethnie, type_c in questions:
        console.print(f"[bold cyan]❓ {question}[/bold cyan]")

        filtres = []
        if ethnie:   filtres.append(f"ethnie={ethnie.value}")
        if type_c:   filtres.append(f"type={type_c.value}")
        if filtres:  console.print(f"   [dim]Filtres : {', '.join(filtres)}[/dim]")

        resultats = r.rechercher(
            question=question,
            nb_resultats=2,
            filtre_ethnie=ethnie,
            filtre_type=type_c,
        )

        if not resultats:
            console.print("   [red]Aucun résultat pertinent trouvé[/red]\n")
            continue

        table = Table(box=box.SIMPLE, show_header=True, header_style="dim")
        table.add_column("Score", width=7, justify="center")
        table.add_column("Titre", width=35)
        table.add_column("Ethnie", width=10)
        table.add_column("Type", width=10)
        table.add_column("Extrait", width=50)

        for res in resultats:
            score_color = "green" if res.score > 0.55 else "yellow" if res.score > 0.40 else "red"
            table.add_row(
                f"[{score_color}]{res.score}[/{score_color}]",
                res.titre_parent,
                res.ethnie.value,
                res.type_contenu.value,
                res.contenu[:80] + "..." if len(res.contenu) > 80 else res.contenu,
            )

        console.print(table)