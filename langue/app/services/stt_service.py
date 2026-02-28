import tempfile
import os
import numpy as np
import wave


class WhisperSTTService:
    def __init__(self):
        self._model = None

    def _get_model(self):
        if self._model is None:
            import whisper
            print("[INIT] Chargement Whisper 'base'...")
            self._model = whisper.load_model("base")
            print("[OK] Whisper pret!")
        return self._model

    def transcribe(self, audio_bytes: bytes, language: str = None) -> dict:
        """Transcrit un audio en texte avec Whisper"""
        model = self._get_model()

        # Create temp file and close it before Whisper reads it (Windows fix)
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp_path = tmp.name
        try:
            tmp.write(audio_bytes)
            tmp.close()  # Close file so Whisper can read it on Windows

            # Load audio with wave and convert to numpy array
            # Whisper expects 16kHz mono float32 array normalized to [-1, 1]
            with wave.open(tmp_path, 'rb') as wf:
                sample_rate = wf.getframerate()
                n_frames = wf.getnframes()
                audio_data = wf.readframes(n_frames)
                
                # Convert to numpy array
                if wf.getsampwidth() == 2:  # 16-bit PCM
                    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                elif wf.getsampwidth() == 4:  # 32-bit PCM
                    audio_np = np.frombuffer(audio_data, dtype=np.int32).astype(np.float32) / 2147483648.0
                else:
                    audio_np = np.frombuffer(audio_data, dtype=np.uint8).astype(np.float32) / 128.0 - 1.0
            
            # Resample to 16kHz if needed
            if sample_rate != 16000:
                # Simple resampling (for better quality, use scipy.signal.resample)
                duration = len(audio_np) / sample_rate
                target_length = int(duration * 16000)
                audio_np = np.interp(
                    np.linspace(0, len(audio_np), target_length),
                    np.arange(len(audio_np)),
                    audio_np
                )

            # Pour le Dioula, on laisse Whisper détecter automatiquement.
            # "fr" donne souvent de meilleurs résultats pour les langues
            # d'Afrique de l'Ouest à écriture latine.
            options = {
                "task": "transcribe",
                "fp16": False,
            }
            if language:
                options["language"] = language

            # Pass numpy array instead of file path (avoids ffmpeg dependency)
            result = model.transcribe(audio_np, **options)
            return {
                "text": result["text"].strip(),
                "language": result.get("language", "unknown"),
            }
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def transcribe_dioula(self, audio_bytes: bytes) -> str:
        """Transcription pour le Dioula (auto-détection de langue)"""
        result = self.transcribe(audio_bytes, language=None)
        return result["text"]


stt_service = WhisperSTTService()
