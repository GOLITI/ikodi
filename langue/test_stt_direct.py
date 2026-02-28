"""Test direct du service STT"""
import sys
import traceback
from pathlib import Path

# Generate synthetic audio
import wave
import struct
import math

def generate_test_wav():
    sample_rate = 16000
    duration = 1
    frequency = 440
    
    wav_path = "test_direct.wav"
    with wave.open(wav_path, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(int(sample_rate * duration)):
            value = int(32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            wav_file.writeframes(struct.pack('<h', value))
    
    return wav_path

print("[1] Generation audio test...")
wav_path = generate_test_wav()
print(f"    Audio cree: {wav_path}")

print("\n[2] Lecture fichier audio...")
with open(wav_path, "rb") as f:
    audio_bytes = f.read()
print(f"    Taille: {len(audio_bytes)} bytes")

print("\n[3] Import service STT...")
from app.services.stt_service import stt_service

print("\n[4] Transcription...")
try:
    result = stt_service.transcribe_dioula(audio_bytes)
    print(f"    ✓ SUCCESS!")
    print(f"    Transcription: '{result}'")
except Exception as e:
    print(f"    ✗ ERREUR: {e}")
    print("\n=== TRACEBACK COMPLET ===")
    traceback.print_exc()
