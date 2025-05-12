from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.whisper_module import transcribe_with_whisper
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
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await fichier.read())
        audio_path = tmp.name

    langue_detectee = detect_language(texte_cible)

    transcription = transcribe_with_whisper(audio_path)
    moteur_utilise = "whisper"

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
