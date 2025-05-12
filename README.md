# IA Prononciation Server

Un serveur FastAPI permettant d'analyser la prononciation d'un enregistrement audio en comparant avec une phrase cible.

## Fonctionnalités
- Détection automatique de la langue (via `langdetect`)
- Transcription avec Whisper
- Comparaison de la transcription avec la phrase attendue
- Calcul d'un score de prononciation et retour pédagogique

## Installation locale
```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Exemple d'appel API
**POST** `/analyse-prononciation`
- `fichier` : fichier audio (.wav, .mp3)
- `texte_cible` : texte attendu
- `moteur` : `whisper`
