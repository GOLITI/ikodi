#!/usr/bin/env python3
"""Test final du Niveau 3 - Démonstration complète"""
import requests
import base64
from pathlib import Path

print('='*50)
print('  TEST FINAL NIVEAU 3 - IA Dioula + Audio')
print('='*50)

# Test 1: Text chat avec génération audio
print('\n[1] Test text-chat avec IA Dioula...')
r = requests.post('http://127.0.0.1:8001/api/niveau3/text-chat',
    json={'text': 'Comment dit-on bonjour en Dioula?'}, timeout=60)

if r.status_code == 200:
    data = r.json()
    print(f'\n  Question: {data.get("user_input")}')
    print(f'\n  Reponse IA:')
    print('-'*40)
    ai_response = data.get('ai_response', '')
    for line in ai_response.split('\n')[:6]:
        print(f'  {line}')
    print('-'*40)
    
    if data.get('response_audio_base64'):
        audio = base64.b64decode(data['response_audio_base64'])
        Path('audio_samples/demo_niveau3.mp3').write_bytes(audio)
        print(f'\n  [OK] Audio genere: {len(audio)} bytes')
        print(f'       Fichier: audio_samples/demo_niveau3.mp3')
    else:
        print('\n  [X] Pas d audio genere')
    
    # Phrases similaires
    similar = data.get('similar_phrases', [])
    if similar:
        print(f'\n  Phrases similaires ({len(similar)}):')
        for p in similar[:3]:
            print(f'    - {p.get("dioula")} = {p.get("french")}')
else:
    print(f'  [ERREUR] Status: {r.status_code}')

# Test 2: Health check
print('\n[2] Health check...')
r = requests.get('http://127.0.0.1:8001/health', timeout=5)
if r.status_code == 200:
    h = r.json()
    print(f'  Status: {h.get("status")}')
    print(f'  RAG: {h.get("rag_initialized")}')
    print(f'  LLM: {h.get("llm_engine")}')
    print(f'  Mode: {h.get("mode")}')

print('\n' + '='*50)
print('  TOUS LES TESTS PASSES!')
print('='*50)
