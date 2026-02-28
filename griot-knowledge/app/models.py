"""
GriotKnowledge — models.py
===========================
Schémas de données Pydantic pour tout le système.

Hiérarchie :
    Conte / Proverbe  →  Document  →  Chunk  →  VectorRecord
    (source brute)       (normalisé)   (découpé)   (stocké dans Qdrant)
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


# ─────────────────────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────────────────────

class TypeContenu(str, Enum):
    """Type de contenu culturel."""
    CONTE       = "conte"
    PROVERBE    = "proverbe"
    LEGENDE     = "legende"
    CHANT       = "chant"
    RITUEL      = "rituel"


class Langue(str, Enum):
    """Langues supportées."""
    FRANCAIS    = "fr"
    BAOULE      = "baoule"
    DIOULA      = "dioula"
    SENOUFO     = "senoufo"
    BETE        = "bete"
    AGNI        = "agni"
    AUTRE       = "autre"


class Ethnie(str, Enum):
    """Groupes ethniques ivoiriens."""
    ABBEY       = "abbey"
    AGNI        = "agni"
    AKAN        = "akan"
    BAOULE      = "baoulé"
    BETE        = "bété"
    DIOULA      = "dioula"
    GOURO       = "gouro"
    LOBI        = "lobi"
    MALINKE     = "malinké"
    SENOUFO     = "sénoufo"
    WOBE        = "wobè"
    YACOUBA     = "yacouba"
    AUTRE       = "autre"


# ─────────────────────────────────────────────────────────────
# DOCUMENT SOURCE  (ce que l'on collecte auprès des griots)
# ─────────────────────────────────────────────────────────────

class DocumentSource(BaseModel):
    """
    Représente un conte ou proverbe brut,
    tel que collecté sur le terrain.
    """
    id: str = Field(
        description="Identifiant unique. Ex: 'baou_conte_001'"
    )
    titre: str = Field(
        description="Titre du conte ou début du proverbe"
    )
    contenu: str = Field(
        description="Texte complet du conte ou proverbe"
    )
    type_contenu: TypeContenu = Field(
        description="Nature du contenu culturel"
    )
    langue: Langue = Field(
        default=Langue.FRANCAIS,
        description="Langue du contenu"
    )
    ethnie: Ethnie = Field(
        description="Groupe ethnique d'origine"
    )
    region: Optional[str] = Field(
        default=None,
        description="Région géographique. Ex: 'Yamoussoukro', 'Bouaké'"
    )
    morale: Optional[str] = Field(
        default=None,
        description="Enseignement ou morale du conte"
    )
    themes: list[str] = Field(
        default=[],
        description="Thèmes abordés. Ex: ['courage', 'famille', 'nature']"
    )
    source_collecte: Optional[str] = Field(
        default=None,
        description="Nom du griot ou dépositaire du savoir"
    )
    date_collecte: Optional[datetime] = Field(
        default=None,
        description="Date de collecte du témoignage"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "baou_conte_001",
                "titre": "L'araignée et le lion",
                "contenu": "Il était une fois, dans la grande forêt du Baoulé...",
                "type_contenu": "conte",
                "langue": "fr",
                "ethnie": "baoulé",
                "region": "Yamoussoukro",
                "morale": "La ruse l'emporte sur la force brute.",
                "themes": ["ruse", "courage", "animaux"],
                "source_collecte": "Griot Konan Yao",
                "date_collecte": "2024-03-15T10:00:00"
            }
        }
    }


# ─────────────────────────────────────────────────────────────
# CHUNK  (fragment découpé pour l'embedding)
# ─────────────────────────────────────────────────────────────

class Chunk(BaseModel):
    """
    Fragment d'un DocumentSource après découpage.
    C'est l'unité réelle stockée dans Qdrant avec son vecteur.
    """
    chunk_id: str = Field(
        description="ID unique du chunk. Ex: 'baou_conte_001_chunk_0'"
    )
    doc_id: str = Field(
        description="ID du DocumentSource parent"
    )
    contenu: str = Field(
        description="Texte du fragment"
    )
    position: int = Field(
        description="Index du chunk dans le document parent (0, 1, 2...)"
    )
    # Métadonnées héritées du parent (pour filtrer dans Qdrant)
    type_contenu: TypeContenu
    langue: Langue
    ethnie: Ethnie
    region: Optional[str] = None
    themes: list[str] = []
    morale: Optional[str] = None
    titre_parent: str = Field(
        description="Titre du document parent (pour affichage)"
    )


# ─────────────────────────────────────────────────────────────
# REQUÊTE UTILISATEUR
# ─────────────────────────────────────────────────────────────

class RequeteUtilisateur(BaseModel):
    """
    Question posée par l'utilisateur à GriotKnowledge.
    """
    question: str = Field(
        description="La question ou situation de l'utilisateur",
        min_length=3,
        max_length=1000
    )
    langue_reponse: Langue = Field(
        default=Langue.FRANCAIS,
        description="Langue souhaitée pour la réponse"
    )
    filtre_ethnie: Optional[Ethnie] = Field(
        default=None,
        description="Filtrer les résultats sur une ethnie spécifique"
    )
    filtre_type: Optional[TypeContenu] = Field(
        default=None,
        description="Filtrer sur un type de contenu (conte, proverbe...)"
    )
    nb_resultats: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Nombre de documents sources à récupérer"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "Comment gérer un conflit entre voisins selon la sagesse ivoirienne ?",
                "langue_reponse": "fr",
                "filtre_ethnie": None,
                "filtre_type": "proverbe",
                "nb_resultats": 3
            }
        }
    }


# ─────────────────────────────────────────────────────────────
# RÉSULTAT DE RECHERCHE
# ─────────────────────────────────────────────────────────────

class ResultatRecherche(BaseModel):
    """
    Un document retrouvé dans Qdrant avec son score de similarité.
    """
    chunk_id: str
    doc_id: str
    contenu: str
    titre_parent: str
    ethnie: Ethnie
    type_contenu: TypeContenu
    morale: Optional[str]
    score: float = Field(
        description="Score de similarité cosinus (0 à 1, plus c'est proche de 1, mieux c'est)"
    )


# ─────────────────────────────────────────────────────────────
# RÉPONSE FINALE  (ce que l'API retourne à l'utilisateur)
# ─────────────────────────────────────────────────────────────

class ReponseGriot(BaseModel):
    """
    Réponse finale de GriotKnowledge :
    texte généré par le LLM + sources utilisées.
    """
    question: str = Field(
        description="La question d'origine"
    )
    reponse: str = Field(
        description="Réponse générée par le LLM, ancrée sur les sources"
    )
    sources: list[ResultatRecherche] = Field(
        description="Documents sources utilisés pour générer la réponse"
    )
    nb_sources: int = Field(
        description="Nombre de sources utilisées"
    )
    langue_reponse: Langue

    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "Comment gérer un conflit entre voisins ?",
                "reponse": "Selon la sagesse Baoulé, 'Quand deux éléphants se battent...'",
                "sources": [],
                "nb_sources": 2,
                "langue_reponse": "fr"
            }
        }
    }


# ─────────────────────────────────────────────────────────────
# STATUT D'INGESTION  (retourné par le script ingest.py)
# ─────────────────────────────────────────────────────────────

class StatutIngestion(BaseModel):
    """Résultat d'une opération d'ingestion de corpus."""
    documents_traites: int
    chunks_crees: int
    vecteurs_stockes: int
    erreurs: list[str] = []
    succes: bool