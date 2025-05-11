from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.whisper_module import transcribe_with_whisper
from app.vosk_module import transcribe_with_vosk
from app.utils import compare_texts, detect_language
from pydantic import BaseModel
import tempfile

app = FastAPI()

class AnalyseResult(BaseModel):
    moteur_utilise: str
    langue_detectee: str
    transcription: str
    attendu: str
    score: float
    erreurs: list[str]
    message: str

@app.post("/analyse-prononciation", response_model=AnalyseResult)
async def analyse_prononciation(
    fichier: UploadFile = File(...),
    texte_cible: str = Form(...),
    moteur: str = Form("auto")  # auto, whisper, vosk
):
    # Sauvegarde temporaire du fichier audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await fichier.read())
        audio_path = tmp.name

    # Détection de langue
    langue_detectee = detect_language(texte_cible)

    # Choix du moteur
    if moteur == "auto":
        moteur_utilise = "whisper" if langue_detectee not in ["en", "fr", "de", "es", "ru"] else "vosk"
    else:
        moteur_utilise = moteur

    if moteur_utilise == "whisper":
        transcription = transcribe_with_whisper(audio_path)
    elif moteur_utilise == "vosk":
        transcription = transcribe_with_vosk(audio_path, langue_detectee)
    else:
        return JSONResponse(status_code=400, content={"error": "Moteur inconnu."})

    score, erreurs, message = compare_texts(transcription, texte_cible)

    return AnalyseResult(
        moteur_utilise=moteur_utilise,
        langue_detectee=langue_detectee,
        transcription=transcription,
        attendu=texte_cible,
        score=score,
        erreurs=erreurs,
        message=message
    )
