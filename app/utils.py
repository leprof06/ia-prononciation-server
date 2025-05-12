from difflib import SequenceMatcher
from langdetect import detect
import os
from gtts import gTTS
import json
import random

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "und"

def compare_texts(transcription: str, attendu: str):
    transcription_clean = transcription.lower().strip()
    attendu_clean = attendu.lower().strip()
    ratio = SequenceMatcher(None, transcription_clean, attendu_clean).ratio()
    erreurs = []

    for i, (a, b) in enumerate(zip(attendu_clean, transcription_clean)):
        if a != b:
            erreurs.append(f"Position {i+1}: attendu '{a}', reçu '{b}'")

    message = "Bonne prononciation !" if ratio > 0.9 else "Tu peux encore améliorer ta prononciation."
    return round(ratio * 100, 2), erreurs, message

def generer_tts(texte: str, langue: str) -> str:
    try:
        tts = gTTS(text=texte, lang=langue)
        filename = "static/tts_output.mp3"
        os.makedirs("static", exist_ok=True)
        tts.save(filename)
        return f"https://ia-prononciation-server.onrender.com/{filename}"
    except:
        return None

def get_or_create_tts(texte: str, langue: str) -> str:
    os.makedirs("static", exist_ok=True)
    filename = f"static/{langue}_{hash_text(texte)}.mp3"
    if not os.path.exists(filename):
        try:
            tts = gTTS(text=texte, lang=langue)
            tts.save(filename)
        except:
            return None
    return f"https://ia-prononciation-server.onrender.com/{filename}"

def hash_text(text: str) -> str:
    import hashlib
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def detect_pronunciation_tips(transcription: str, attendu: str, langue: str):
    tips = []
    if langue == "fr":
        if "r" in attendu and "r" not in transcription:
            tips.append("Fais attention à bien prononcer les 'r' français, au fond de la gorge.")
        if "u" in attendu and "u" not in transcription:
            tips.append("Ne confonds pas le 'u' français avec le 'ou'. Le 'u' est plus fermé.")
    elif langue == "en":
        if "th" in attendu and "s" in transcription:
            tips.append("Le 'th' anglais se prononce avec la langue entre les dents, pas comme un 's'.")
    return tips if tips else None

def load_random_phrase(langue: str, niveau: str) -> str:
    os.makedirs("phrases", exist_ok=True)
    filepath = f"phrases/{langue.lower()}_{niveau.lower()}.json"

    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return "Aucune phrase disponible pour cette langue. Tu peux en proposer une !"

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            phrases = json.load(f)
        if not phrases:
            return "Aucune phrase enregistrée pour cette langue. Tu peux en ajouter une toi-même."
        return random.choice(phrases)
    except:
        return "Je suis prêt à t'aider à pratiquer ta prononciation !"

def add_phrase(langue: str, niveau: str, phrase: str) -> str:
    os.makedirs("phrases", exist_ok=True)
    filepath = f"phrases/{langue.lower()}_{niveau.lower()}.json"

    try:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                phrases = json.load(f)
        else:
            phrases = []

        if phrase in phrases:
            return "Cette phrase est déjà enregistrée."

        phrases.append(phrase)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(phrases, f, ensure_ascii=False, indent=2)
        return "Phrase ajoutée avec succès !"

    except Exception as e:
        return f"Erreur lors de l'ajout : {str(e)}"
