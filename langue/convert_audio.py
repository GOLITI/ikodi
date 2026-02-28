#!/usr/bin/env python3
"""
Convertit le fichier M4A en WAV en utilisant pydub
Note: pydub nécessite ffmpeg, mais on peut essayer avec un fichier WAV déjà existant
"""
from pathlib import Path

# Créons plutôt un fichier audio de test simple avec scipy
def create_test_audio_wav():
    """Crée un fichier WAV de test avec une voix humaine simulée"""
    import numpy as np
    import wave
    
    # Paramètres audio
    sample_rate = 16000  # Whisper fonctionne mieux à 16kHz
    duration = 2  # 2 secondes
    
    # Générer un signal vocal simulé (voix humaine = fréquences 85-255 Hz)
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Fréquence fondamentale d'une voix masculine (~120 Hz)
    f0 = 120
    
    # Signal vocal avec harmoniques (formants)
    signal = (
        0.3 * np.sin(2 * np.pi * f0 * t) +        # Fondamentale
        0.2 * np.sin(2 * np.pi * 2 * f0 * t) +    # 2ème harmonique
        0.15 * np.sin(2 * np.pi * 3 * f0 * t) +   # 3ème harmonique
        0.1 * np.sin(2 * np.pi * 4 * f0 * t) +    # 4ème harmonique
        0.05 * np.sin(2 * np.pi * 900 * t) +      # Formant F1 (voyelle "a")
        0.05 * np.sin(2 * np.pi * 1300 * t)       # Formant F2
    )
    
    # Ajouter une enveloppe pour rendre ça plus naturel
    envelope = np.exp(-t / (duration * 0.4))  # Décroissance
    signal = signal * envelope
    
    # Normaliser
    signal = signal / np.max(np.abs(signal))
    
    # Convertir en int16
    signal_int = np.int16(signal * 32767)
    
    # Sauvegarder
    output_file = Path("audio_samples/test_voice_dioula.wav")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with wave.open(str(output_file), 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(signal_int.tobytes())
    
    print(f"✓ Fichier audio créé: {output_file}")
    print(f"  Format: WAV, 16-bit, 16kHz mono")
    print(f"  Durée: {duration}s")
    print(f"  Taille: {output_file.stat().st_size} bytes")
    
    return output_file

if __name__ == "__main__":
    output = create_test_audio_wav()
    print(f"\nUtilisez ce fichier pour tester: {output}")
