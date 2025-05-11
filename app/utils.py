from difflib import SequenceMatcher
from langdetect import detect


def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "unknown"


def compare_texts(transcription: str, target: str):
    transcription = transcription.lower().strip()
    target = target.lower().strip()

    ratio = SequenceMatcher(None, transcription, target).ratio()
    score = round(ratio * 100, 2)

    transcription_words = set(transcription.split())
    target_words = set(target.split())
    errors = list(target_words - transcription_words)

    if score > 90:
        message = "Excellent, ta prononciation est très proche du modèle."
    elif score > 70:
        message = "Bonne tentative, mais certains mots sont à corriger."
    else:
        message = "Essaie encore, plusieurs mots semblent mal prononcés."

    return score, errors, message
