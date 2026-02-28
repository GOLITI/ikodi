"""
GriotKnowledge — ingest.py
============================
Script d'ingestion du corpus culturel ivoirien.

Responsabilités :
    1. Lire les fichiers JSON du dossier data/corpus/
    2. Valider chaque document avec Pydantic (DocumentSource)
    3. Nettoyer la collection Qdrant existante (reset propre)
    4. Indexer tout le corpus via le Vectorizer
    5. Afficher un rapport d'ingestion

Utilisation :
    python scripts/ingest.py               ← ingère tout le corpus
    python scripts/ingest.py --reset       ← supprime et recrée la collection
    python scripts/ingest.py --dry-run     ← valide sans indexer
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich import box

# Ajouter le répertoire racine au path pour importer app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models import DocumentSource, TypeContenu, Langue, Ethnie, StatutIngestion
from app.vectorizer import Vectorizer, COLLECTION_NAME

load_dotenv()
console = Console()

CORPUS_PATH = Path("data/corpus")


# ─────────────────────────────────────────────────────────────
# CORPUS DE DÉMONSTRATION
# Créé automatiquement si data/corpus/ est vide
# ─────────────────────────────────────────────────────────────

CORPUS_DEMO = [
    {
        "id": "baou_conte_001",
        "titre": "La tortue et l'aigle",
        "contenu": (
            "Il était une fois, dans la grande forêt du Baoulé, une tortue qui rêvait de voler. "
            "Tous les animaux se moquaient d'elle. 'Tu n'as pas d'ailes', lui disait le singe. "
            "'Tu es trop lourde', riait le perroquet. Mais la tortue ne se découragea pas. "
            "Elle observa l'aigle pendant des semaines, étudiant chaque battement d'aile. "
            "Un jour, elle demanda à l'aigle de l'emmener dans les airs. L'aigle, touché par "
            "sa persévérance, accepta. Ensemble, ils survolèrent la forêt. La tortue comprit "
            "alors que voler ne voulait pas dire avoir des ailes, mais avoir la volonté "
            "de s'élever par tous les moyens."
        ),
        "type_contenu": "conte",
        "langue": "fr",
        "ethnie": "baoulé",
        "region": "Yamoussoukro",
        "morale": "La persévérance et l'humilité ouvrent des portes que la force seule ne peut forcer.",
        "themes": ["persévérance", "humilité", "rêve", "amitié"],
        "source_collecte": "Griot Konan Yao"
    },
    {
        "id": "baou_prov_001",
        "titre": "Proverbe sur la parole",
        "contenu": (
            "La parole est comme l'oeuf : une fois tombée, elle se brise et ne peut être "
            "ramassée. C'est pourquoi le sage réfléchit sept fois avant d'ouvrir la bouche, "
            "car les mots blessants laissent des cicatrices que le temps efface difficilement."
        ),
        "type_contenu": "proverbe",
        "langue": "fr",
        "ethnie": "baoulé",
        "region": "Bouaké",
        "morale": "Réfléchir avant de parler évite bien des conflits.",
        "themes": ["parole", "sagesse", "relations", "prudence"],
        "source_collecte": "Griot Konan Yao"
    },
    {
        "id": "diou_conte_001",
        "titre": "L'araignée et le roi des animaux",
        "contenu": (
            "Dans le temps ancien, l'araignée Ananse voulait posséder toutes les histoires "
            "du monde. Elle alla trouver Nyame, le dieu du ciel, et lui demanda son prix. "
            "Nyame exigea trois choses impossibles : capturer le python royal, attraper les "
            "frelons furieux, et saisir le léopard invisible. Ananse, par sa ruse et son "
            "intelligence, accomplit les trois épreuves là où la force avait échoué. "
            "Depuis ce jour, toutes les histoires du monde appartiennent à l'araignée, "
            "et c'est pourquoi on les appelle les 'histoires d'Ananse'."
        ),
        "type_contenu": "conte",
        "langue": "fr",
        "ethnie": "agni",
        "region": "Abengourou",
        "morale": "L'intelligence et la ruse triomphent là où la force échoue.",
        "themes": ["ruse", "intelligence", "défi", "connaissance"],
        "source_collecte": "Dépositaire Ama Adjoua"
    },
    {
        "id": "diou_prov_001",
        "titre": "Proverbe sur l'unité",
        "contenu": (
            "Quand les termites s'unissent, elles peuvent déplacer un éléphant. "
            "Une seule termite ne peut rien contre la peau épaisse de la bête, "
            "mais mille termites agissant ensemble peuvent venir à bout du plus grand obstacle. "
            "C'est la leçon que les anciens nous ont transmise : seul on va vite, "
            "ensemble on va loin."
        ),
        "type_contenu": "proverbe",
        "langue": "fr",
        "ethnie": "dioula",
        "region": "Korhogo",
        "morale": "L'union fait la force. La solidarité communautaire dépasse la capacité individuelle.",
        "themes": ["unité", "solidarité", "communauté", "force collective"],
        "source_collecte": "Griot Mamadou Coulibaly"
    },
    {
        "id": "senoufo_conte_001",
        "titre": "Le forgeron et l'esprit du fer",
        "contenu": (
            "Chez les Sénoufo, le forgeron n'est pas un simple artisan : il est l'intermédiaire "
            "entre le monde des vivants et celui des esprits. Il était une fois un jeune forgeron "
            "nommé Siaka qui voulait créer le plus beau masque Kpelié jamais vu. "
            "Pendant sept nuits, il travailla sans relâche, mais le métal refusait de prendre "
            "la forme voulue. La huitième nuit, l'esprit du fer lui apparut et lui dit : "
            "'Tu cherches la beauté dans tes mains, mais elle est dans ton cœur.' "
            "Siaka comprit alors qu'il devait d'abord purifier ses intentions avant de toucher "
            "le métal. Il pria, jeûna, et médita. Le neuvième jour, le masque se créa "
            "presque seul, plus beau qu'il n'avait jamais espéré."
        ),
        "type_contenu": "conte",
        "langue": "fr",
        "ethnie": "sénoufo",
        "region": "Korhogo",
        "morale": "La pureté d'intention précède la maîtrise technique. L'artisan doit d'abord travailler son âme.",
        "themes": ["artisanat", "spiritualité", "intention", "patience", "masque"],
        "source_collecte": "Maître forgeron Soro Navigué"
    },
    {
        "id": "bete_prov_001",
        "titre": "Proverbe sur le conflit",
        "contenu": (
            "Quand deux éléphants se battent, c'est l'herbe qui souffre. "
            "Les grands de ce monde oublient souvent que leurs querelles "
            "écrasent les petits qui n'ont rien à y gagner. "
            "Le sage cherche toujours à réconcilier avant que la bataille commence, "
            "car une fois que les éléphants chargent, même la forêt tremble."
        ),
        "type_contenu": "proverbe",
        "langue": "fr",
        "ethnie": "bété",
        "region": "Daloa",
        "morale": "Les conflits entre puissants nuisent toujours aux plus faibles. La paix vaut mieux que la victoire.",
        "themes": ["conflit", "paix", "justice", "pouvoir", "responsabilité"],
        "source_collecte": "Chef de village Gnahoré Bi"
    },
    {
        "id": "baou_conte_002",
        "titre": "La rivière qui refusait de couler",
        "contenu": (
            "Dans le village de Kossou, la rivière s'arrêta de couler un jour sans raison. "
            "Les villageois avaient soif, les récoltes mouraient. Les anciens consultèrent "
            "l'oracle qui leur dit : 'La rivière est en colère car vous avez oublié de "
            "la remercier.' Personne ne comprenait. Puis une vieille femme se souvint : "
            "autrefois, chaque matin, les habitants versaient une calebasse d'eau dans la "
            "rivière en signe de gratitude. Cette tradition s'était perdue avec les jeunes "
            "générations. Les villageois reprirent le rituel. Le lendemain, la rivière "
            "coulait à nouveau, plus abondante qu'avant."
        ),
        "type_contenu": "conte",
        "langue": "fr",
        "ethnie": "baoulé",
        "region": "Kossou",
        "morale": "La gratitude envers la nature est un devoir, pas une option. Ce que nos ancêtres ont construit, nous devons l'entretenir.",
        "themes": ["gratitude", "tradition", "nature", "mémoire", "rituel", "eau"],
        "source_collecte": "Griot Konan Yao"
    },
    {
        "id": "diou_prov_002",
        "titre": "Proverbe sur la patience",
        "contenu": (
            "Le bois qu'on veut courber doit d'abord être chauffé doucement. "
            "Celui qui force trop vite casse ce qu'il voulait façonner. "
            "La patience n'est pas la faiblesse : c'est la sagesse de comprendre "
            "que chaque chose a son temps, et que précipiter les choses "
            "revient souvent à tout recommencer depuis le début."
        ),
        "type_contenu": "proverbe",
        "langue": "fr",
        "ethnie": "dioula",
        "region": "Odienné",
        "morale": "La patience est la mère de toutes les vertus. Rien de grand ne se construit dans la précipitation.",
        "themes": ["patience", "sagesse", "travail", "temps", "méthode"],
        "source_collecte": "Griot Mamadou Coulibaly"
    },
]


# ─────────────────────────────────────────────────────────────
# FONCTIONS
# ─────────────────────────────────────────────────────────────

def creer_corpus_demo():
    """Crée les fichiers JSON de démonstration dans data/corpus/."""
    CORPUS_PATH.mkdir(parents=True, exist_ok=True)

    # Regrouper par ethnie
    par_ethnie: dict[str, list] = {}
    for doc in CORPUS_DEMO:
        ethnie = doc["ethnie"]
        par_ethnie.setdefault(ethnie, []).append(doc)

    for ethnie, docs in par_ethnie.items():
        fichier = CORPUS_PATH / f"{ethnie.replace('é', 'e').replace('ô', 'o')}.json"
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(docs, f, ensure_ascii=False, indent=2)
        console.print(f"  📁 Créé : {fichier} ({len(docs)} document(s))")


def charger_corpus() -> list[DocumentSource]:
    """Lit tous les fichiers JSON de data/corpus/ et retourne une liste de DocumentSource."""
    if not CORPUS_PATH.exists() or not list(CORPUS_PATH.glob("*.json")):
        console.print("[yellow]⚠️  Corpus vide — génération du corpus de démonstration...[/yellow]")
        creer_corpus_demo()

    documents = []
    erreurs = []

    for fichier in sorted(CORPUS_PATH.glob("*.json")):
        try:
            with open(fichier, encoding="utf-8") as f:
                data = json.load(f)

            # Accepte un objet unique ou une liste
            if isinstance(data, dict):
                data = [data]

            for item in data:
                try:
                    doc = DocumentSource(**item)
                    documents.append(doc)
                except Exception as e:
                    erreurs.append(f"{fichier.name} → {e}")

        except Exception as e:
            erreurs.append(f"{fichier.name} → {e}")

    if erreurs:
        console.print(f"[red]❌ {len(erreurs)} erreur(s) de validation :[/red]")
        for e in erreurs:
            console.print(f"   [red]{e}[/red]")

    return documents


def afficher_rapport(documents: list[DocumentSource], statut: StatutIngestion):
    """Affiche un tableau récapitulatif de l'ingestion."""

    # Tableau par ethnie
    table = Table(
        title="📊 Corpus indexé",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold yellow"
    )
    table.add_column("Ethnie", style="cyan")
    table.add_column("Contes", justify="center")
    table.add_column("Proverbes", justify="center")
    table.add_column("Autres", justify="center")
    table.add_column("Total", justify="center", style="bold")

    stats: dict[str, dict] = {}
    for doc in documents:
        e = doc.ethnie.value
        stats.setdefault(e, {"conte": 0, "proverbe": 0, "autre": 0})
        if doc.type_contenu == TypeContenu.CONTE:
            stats[e]["conte"] += 1
        elif doc.type_contenu == TypeContenu.PROVERBE:
            stats[e]["proverbe"] += 1
        else:
            stats[e]["autre"] += 1

    for ethnie, s in sorted(stats.items()):
        total = s["conte"] + s["proverbe"] + s["autre"]
        table.add_row(ethnie, str(s["conte"]), str(s["proverbe"]), str(s["autre"]), str(total))

    console.print(table)

    # Résumé
    couleur = "green" if statut.succes else "yellow"
    console.print(Panel(
        f"[bold]Documents traités :[/bold] {statut.documents_traites}\n"
        f"[bold]Chunks créés      :[/bold] {statut.chunks_crees}\n"
        f"[bold]Vecteurs stockés  :[/bold] {statut.vecteurs_stockes}\n"
        f"[bold]Erreurs           :[/bold] {len(statut.erreurs)}\n"
        f"[bold]Statut            :[/bold] {'✅ Succès' if statut.succes else '⚠️  Partiel'}",
        title="Résumé ingestion",
        border_style=couleur
    ))


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Ingestion du corpus GriotKnowledge")
    parser.add_argument("--reset",   action="store_true", help="Supprime et recrée la collection Qdrant")
    parser.add_argument("--dry-run", action="store_true", help="Valide les documents sans indexer")
    args = parser.parse_args()

    console.print(Panel.fit(
        "[bold yellow]🥁 GriotKnowledge — Ingestion du Corpus[/bold yellow]\n"
        "[dim]Chargement des contes et proverbes ivoiriens dans Qdrant[/dim]",
        border_style="yellow"
    ))

    # 1. Charger le corpus
    console.print("\n[bold]📂 Chargement du corpus...[/bold]")
    documents = charger_corpus()

    if not documents:
        console.print("[red]❌ Aucun document trouvé. Vérifiez data/corpus/[/red]")
        return

    console.print(f"  ✅ {len(documents)} document(s) chargé(s) et validé(s)")

    # 2. Mode dry-run : afficher et quitter
    if args.dry_run:
        console.print("\n[yellow]🔍 Mode dry-run — pas d'indexation[/yellow]")
        for doc in documents:
            console.print(f"  ✓ [{doc.ethnie.value}] {doc.titre} ({doc.type_contenu.value})")
        return

    # 3. Initialiser le Vectorizer
    console.print("\n[bold]🔧 Initialisation du Vectorizer...[/bold]")
    vectorizer = Vectorizer()

    # 4. Reset si demandé
    if args.reset:
        console.print(f"\n[yellow]🗑️  Reset de la collection '{COLLECTION_NAME}'...[/yellow]")
        try:
            vectorizer.client.delete_collection(COLLECTION_NAME)
            console.print("  ✅ Collection supprimée")
            vectorizer._creer_collection_si_absente()
        except Exception as e:
            console.print(f"  [red]Erreur reset : {e}[/red]")

    # 5. Indexer
    console.print(f"\n[bold]🚀 Indexation de {len(documents)} document(s)...[/bold]")
    statut = vectorizer.indexer_corpus(documents)

    # 6. Rapport
    console.print()
    afficher_rapport(documents, statut)
    console.print("\n[dim]Vérifiez vos vecteurs sur http://localhost:6333/dashboard[/dim]")


if __name__ == "__main__":
    main()