import os
import hashlib
import re
from pathlib import Path
from io import BytesIO

AUDIO_CACHE_DIR = Path("audio_samples/cache")
AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def clean_text_for_tts(text: str) -> str:
    """Nettoie le texte pour la synthèse vocale (supprime emojis, markdown, etc.)"""
    # Supprimer les emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"  # chess symbols
        "\U0001FA70-\U0001FAFF"  # symbols extended
        "\U00002600-\U000026FF"  # misc symbols
        "\U00002700-\U000027BF"  # dingbats
        "]+", flags=re.UNICODE
    )
    text = emoji_pattern.sub('', text)
    
    # Supprimer les astérisques du markdown (gras: **texte**)
    text = re.sub(r'\*+', '', text)
    
    # Supprimer les underscores du markdown (italique: _texte_)
    text = re.sub(r'_+', ' ', text)
    
    # Supprimer les crochets et leur contenu de type [texte]
    text = re.sub(r'\[([^\]]+)\]', r'\1', text)
    
    # Supprimer les backticks
    text = re.sub(r'`+', '', text)
    
    # Supprimer les dièses (titres markdown)
    text = re.sub(r'#+\s*', '', text)
    
    # Nettoyer les espaces multiples
    text = re.sub(r'\s+', ' ', text)
    
    # Supprimer les espaces en début/fin
    text = text.strip()
    
    return text


class TTSService:
    def __init__(self):
        self._gtts = None

    def text_to_speech(self, text: str) -> bytes:
        """Convertit du texte en audio avec gTTS (gratuit)"""
        # Nettoyer le texte avant synthèse
        clean_text = clean_text_for_tts(text)
        
        cache_key = hashlib.md5(clean_text.encode()).hexdigest()
        cache_file = AUDIO_CACHE_DIR / f"{cache_key}.mp3"

        if cache_file.exists():
            return cache_file.read_bytes()

        try:
            from gtts import gTTS
            
            # gTTS - Gratuit et illimité
            # Utilise 'fr' pour le français (comprend bien le Dioula écrit)
            tts = gTTS(text=clean_text, lang='fr', slow=False)
            
            # Sauvegarder dans un buffer
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_bytes = audio_buffer.getvalue()
            
            # Cache le fichier
            cache_file.write_bytes(audio_bytes)
            print(f"[TTS] Audio genere: {len(audio_bytes)} bytes")
            return audio_bytes
            
        except Exception as e:
            print(f"[TTS ERROR] gTTS: {str(e)}")
            raise

    def generate_lesson_audio(self, dioula: str, french: str) -> bytes:
        """Audio d'une leçon: Dioula + traduction française"""
        combined = f"{dioula}. En français: {french}"
        return self.text_to_speech(combined)


tts_service = TTSService()
