import os
import wave
from vosk import Model, KaldiRecognizer
import json

# Préparer les modèles pour différentes langues si besoin
def get_vosk_model(language_code: str):
    model_paths = {
        "en": "models/vosk-en",
        "fr": "models/vosk-fr",
        "de": "models/vosk-de",
        "es": "models/vosk-es",
        "ru": "models/vosk-ru",
    }
    model_path = model_paths.get(language_code, "models/vosk-en")
    if not os.path.exists(model_path):
        raise RuntimeError(f"Modèle Vosk non trouvé pour {language_code}.")
    return Model(model_path)

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
