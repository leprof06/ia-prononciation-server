from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.whisper_module import transcribe_with_whisper
from app.vosk_module import transcribe_with_vosk, prepare_vosk_model
from app.utils import compare_texts, detect_language
from app.download_models import vosk_models
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
    moteur: str = Form("auto")
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await fichier.read())
        audio_path = tmp.name

    langue_detectee = detect_language(texte_cible)

    if moteur == "auto":
        moteur_utilise = "whisper" if langue_detectee not in vosk_models else "vosk"
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

@app.post("/prepare-modele")
async def preparer_modele(langue: str = Form(...)):
    if langue not in vosk_models:
        return JSONResponse(status_code=400, content={"error": f"Aucun modèle Vosk prévu pour '{langue}'"})
    prepare_vosk_model(langue)
    return {"message": f"Modèle '{langue}' prêt à l'emploi."}
