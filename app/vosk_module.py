import os
import wave
from vosk import Model, KaldiRecognizer
import json
from app.download_models import vosk_models, download_and_extract

# Préparer les modèles pour différentes langues si besoin
def get_vosk_model(language_code: str):
    model_path = os.path.join("models", f"vosk-{language_code}")

    if not os.path.exists(model_path):
        print(f"Modèle manquant pour {language_code}, téléchargement en cours...")
        url = vosk_models.get(language_code)
        if url:
            download_and_extract(language_code, url)
        else:
            raise RuntimeError(f"Aucun modèle disponible pour la langue '{language_code}'")

    return Model(model_path)

# Précharger un modèle sans transcription (utilisé à l'annonce de la langue)
def prepare_vosk_model(language_code: str):
    model_path = os.path.join("models", f"vosk-{language_code}")
    if not os.path.exists(model_path):
        print(f"Préchargement du modèle Vosk pour {language_code}")
        url = vosk_models.get(language_code)
        if url:
            download_and_extract(language_code, url)

# Transcription vocale avec Vosk
def transcribe_with_vosk(audio_path: str, language_code: str) -> str:
    model = get_vosk_model(language_code)
    wf = wave.open(audio_path, "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [16000, 44100]:
        raise ValueError("Le fichier doit être en mono, 16-bit, 16kHz ou 44.1kHz")

    rec = KaldiRecognizer(model, wf.getframerate())
    transcription = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            transcription += " " + res.get("text", "")

    res = json.loads(rec.FinalResult())
    transcription += " " + res.get("text", "")
    return transcription.strip()
