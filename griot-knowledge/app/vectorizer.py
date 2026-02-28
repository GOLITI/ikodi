"""
GriotKnowledge — vectorizer.py
================================
Microservice de vectorisation.

Responsabilités :
    1. Charger le modèle d'embedding multilingue
    2. Découper un DocumentSource en Chunks
    3. Transformer chaque Chunk en vecteur numérique
    4. Créer la collection Qdrant si elle n'existe pas
    5. Stocker les vecteurs + métadonnées dans Qdrant
"""

import os
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
# Import heavy ML deps lazily to allow lightweight Docker image builds
# langchain_text_splitters may not be available in the lightweight image;
# import it lazily in __init__ to avoid startup failure.

try:
    from .models import DocumentSource, Chunk, StatutIngestion
except ImportError:
    from models import DocumentSource, Chunk, StatutIngestion

load_dotenv()


# ─────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────

QDRANT_HOST         = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT         = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME     = os.getenv("QDRANT_COLLECTION_NAME", "griot_corpus")
EMBEDDING_MODEL     = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", 384))

# Taille des chunks : équilibre entre contexte et précision
CHUNK_SIZE          = 400   # caractères par chunk
CHUNK_OVERLAP       = 60    # chevauchement pour ne pas couper le sens


# ─────────────────────────────────────────────────────────────
# VECTORIZER
# ─────────────────────────────────────────────────────────────

class Vectorizer:
    """
    Transforme des DocumentSource en vecteurs stockés dans Qdrant.

    Utilisation :
        vectorizer = Vectorizer()
        statut = vectorizer.indexer_document(mon_conte)
    """

    def __init__(self):
        print(f"⏳ Chargement embedding : {EMBEDDING_MODEL}")
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            print("✅ SentenceTransformer chargé pour le Vectorizer")
        except Exception:
            self.model = None
            print("⚠️  sentence-transformers non installé — vectorizer en mode dégradé")
        try:
            self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
            print(f"✅ Qdrant client initialisé ({QDRANT_HOST}:{QDRANT_PORT})")
        except Exception as e:
            self.client = None
            print(f"⚠️  Impossible de se connecter à Qdrant ({QDRANT_HOST}:{QDRANT_PORT}) : {e}\n    Vectorizer en mode dégradé (indexation désactivée)")
        try:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
                separators=["\n\n", "\n", ".", "!", "?", " "],
            )
        except Exception:
            self.splitter = None
            print("⚠️  langchain_text_splitters non installé — découpage en mode dégradé")
        if self.client is not None:
            try:
                self._creer_collection_si_absente()
                print(f"✅ Vectorizer prêt ({QDRANT_HOST}:{QDRANT_PORT})")
            except Exception as e:
                print(f"⚠️  Erreur lors de la création de la collection Qdrant : {e}")
                self.client = None
                print("    Vectorizer passe en mode dégradé (Qdrant désactivé)")
        else:
            print("⚠️  Vectorizer prêt en mode dégradé (Qdrant indisponible)")

    # ── Collection Qdrant ────────────────────────────────────

    def _creer_collection_si_absente(self):
        """Crée la collection Qdrant si elle n'existe pas encore."""
        collections = [c.name for c in self.client.get_collections().collections]

        if COLLECTION_NAME not in collections:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIMENSION,
                    distance=Distance.COSINE,
                ),
            )
            print(f"✅ Collection '{COLLECTION_NAME}' créée")

    # ── Découpage en chunks ──────────────────────────────────

    def _decouper_en_chunks(self, doc: DocumentSource) -> list[Chunk]:
        """
        Découpe le contenu d'un DocumentSource en fragments.

        Pour les proverbes (courts) : on garde le texte entier en 1 chunk.
        Pour les contes (longs)     : on découpe avec chevauchement.
        """
        # Enrichir le texte avec titre + morale pour améliorer la recherche
        texte_enrichi = doc.contenu
        if doc.morale:
            texte_enrichi = f"{doc.contenu}\n\nMorale : {doc.morale}"

        fragments = self.splitter.split_text(texte_enrichi)

        chunks = []
        for i, fragment in enumerate(fragments):
            chunk = Chunk(
                chunk_id=f"{doc.id}_chunk_{i}",
                doc_id=doc.id,
                contenu=fragment,
                position=i,
                type_contenu=doc.type_contenu,
                langue=doc.langue,
                ethnie=doc.ethnie,
                region=doc.region,
                themes=doc.themes,
                morale=doc.morale,
                titre_parent=doc.titre,
            )
            chunks.append(chunk)

        return chunks

    # ── Embedding ────────────────────────────────────────────

    def _vectoriser(self, textes: list[str]) -> list[list[float]]:
        """Transforme une liste de textes en vecteurs numériques."""
        vecteurs = self.model.encode(
            textes,
            show_progress_bar=len(textes) > 5,
            normalize_embeddings=True,  # normaliser pour la similarité cosinus
        )
        return vecteurs.tolist()

    # ── Stockage dans Qdrant ─────────────────────────────────

    def _stocker_chunks(self, chunks: list[Chunk], vecteurs: list[list[float]]):
        """Insère les chunks et leurs vecteurs dans Qdrant."""
        points = []
        for chunk, vecteur in zip(chunks, vecteurs):
            point = PointStruct(
                id=str(uuid.uuid4()),       # ID unique généré
                vector=vecteur,
                payload={                   # métadonnées filtrables
                    "chunk_id":     chunk.chunk_id,
                    "doc_id":       chunk.doc_id,
                    "contenu":      chunk.contenu,
                    "titre_parent": chunk.titre_parent,
                    "type_contenu": chunk.type_contenu.value,
                    "langue":       chunk.langue.value,
                    "ethnie":       chunk.ethnie.value,
                    "region":       chunk.region,
                    "themes":       chunk.themes,
                    "morale":       chunk.morale,
                    "position":     chunk.position,
                },
            )
            points.append(point)

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )

    # ── Méthode principale ───────────────────────────────────

    def indexer_document(self, doc: DocumentSource) -> dict:
        """
        Pipeline complet pour un seul document :
            DocumentSource → Chunks → Vecteurs → Qdrant

        Retourne un résumé de l'opération.
        """
        print(f"\n📄 Indexation : '{doc.titre}' [{doc.ethnie.value} / {doc.type_contenu.value}]")

        # 1. Découpage
        chunks = self._decouper_en_chunks(doc)
        print(f"   ✂️  {len(chunks)} chunk(s) créé(s)")

        # 2. Vectorisation
        textes = [c.contenu for c in chunks]
        vecteurs = self._vectoriser(textes)
        print(f"   🔢 {len(vecteurs)} vecteur(s) de dimension {len(vecteurs[0])}")

        # 3. Stockage
        self._stocker_chunks(chunks, vecteurs)
        print(f"   💾 Stocké dans Qdrant — collection '{COLLECTION_NAME}'")

        return {
            "doc_id": doc.id,
            "titre": doc.titre,
            "chunks": len(chunks),
            "vecteurs": len(vecteurs),
        }

    def indexer_corpus(self, documents: list[DocumentSource]) -> StatutIngestion:
        """
        Indexe une liste complète de documents (corpus entier).
        Utilisé par ingest.py.
        """
        total_chunks = 0
        erreurs = []

        for doc in documents:
            try:
                resultat = self.indexer_document(doc)
                total_chunks += resultat["chunks"]
            except Exception as e:
                erreurs.append(f"{doc.id} : {str(e)}")
                print(f"   ❌ Erreur sur '{doc.titre}' : {e}")

        statut = StatutIngestion(
            documents_traites=len(documents) - len(erreurs),
            chunks_crees=total_chunks,
            vecteurs_stockes=total_chunks,
            erreurs=erreurs,
            succes=len(erreurs) == 0,
        )

        print(f"\n{'✅' if statut.succes else '⚠️ '} Ingestion terminée :")
        print(f"   Documents traités : {statut.documents_traites}/{len(documents)}")
        print(f"   Chunks stockés    : {statut.chunks_crees}")
        if erreurs:
            print(f"   Erreurs           : {len(erreurs)}")

        return statut

    def supprimer_document(self, doc_id: str):
        """Supprime tous les chunks d'un document par son doc_id."""
        self.client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=Filter(
                must=[FieldCondition(key="doc_id", match=MatchValue(value=doc_id))]
            ),
        )
        print(f"🗑️  Document '{doc_id}' supprimé de Qdrant")

    def stats_collection(self) -> dict:
        """Retourne les statistiques de la collection Qdrant."""
        info = self.client.get_collection(COLLECTION_NAME)
        return {
            "collection": COLLECTION_NAME,
            "nb_vecteurs": info.points_count,
            "dimension": info.config.params.vectors.size,
            "distance": info.config.params.vectors.distance.value,
        }


# ─────────────────────────────────────────────────────────────
# TEST RAPIDE  (python app/vectorizer.py)
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from models import TypeContenu, Langue, Ethnie
    from datetime import datetime

    # Conte de test
    conte_test = DocumentSource(
        id="test_baou_001",
        titre="La tortue et l'aigle",
        contenu=(
            "Il était une fois, dans la grande forêt du Baoulé, une tortue qui rêvait de voler. "
            "Tous les animaux se moquaient d'elle. 'Tu n'as pas d'ailes', lui disait le singe. "
            "'Tu es trop lourde', riait le perroquet. Mais la tortue ne se découragea pas. "
            "Elle observa l'aigle pendant des semaines, étudiant chaque battement d'aile. "
            "Un jour, elle demanda à l'aigle de l'emmener dans les airs. L'aigle, touché par "
            "sa persévérance, accepta. Ensemble, ils survolèrent la forêt. La tortue comprit "
            "alors que voler ne voulait pas dire avoir des ailes, mais avoir la volonté "
            "de s'élever par tous les moyens."
        ),
        type_contenu=TypeContenu.CONTE,
        langue=Langue.FRANCAIS,
        ethnie=Ethnie.BAOULE,
        region="Yamoussoukro",
        morale="La persévérance et l'humilité ouvrent des portes que la force seule ne peut forcer.",
        themes=["persévérance", "humilité", "rêve", "amitié"],
        source_collecte="Griot Konan Yao",
        date_collecte=datetime(2024, 3, 15),
    )

    print("🥁 Test du Vectorizer GriotKnowledge\n")
    v = Vectorizer()

    # Indexer le conte test
    resultat = v.indexer_document(conte_test)

    # Stats
    stats = v.stats_collection()
    print(f"\n📊 Stats collection : {stats}")
    print("\n✅ Vectorizer opérationnel — prochaine étape : ingest.py")
