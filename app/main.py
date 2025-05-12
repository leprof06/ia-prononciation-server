from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.whisper_module import transcribe_with_whisper
from app.utils import compare_texts, detect_language, generer_tts, detect_pronunciation_tips, load_random_phrase, hash_text, get_or_create_tts, add_phrase
from pydantic import BaseModel
from typing import Optional
import tempfile
import os
import base64
import asyncio

app = FastAPI(
    title="IA Prononciation API",
    description="API d'analyse de la prononciation utilisant Whisper",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyseResult(BaseModel):
    moteur_utilise: str
    langue_detectee: str
    transcription: str
    attendu: str
    score: float
    erreurs: list[str]
    message: str
    audio_url: Optional[str] = None
    conseils: Optional[list[str]] = None

@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"message": "Le service est temporairement indisponible. Je fais tout pour résoudre le problème rapidement."})

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyse-prononciation", response_model=AnalyseResult)
async def analyse_prononciation(
    fichier: UploadFile = File(None),
    base64_audio: str = Form(None),
    texte_cible: str = Form(...)
):
    if fichier:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await fichier.read()
            tmp.write(content)
            audio_path = tmp.name
    elif base64_audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(base64.b64decode(base64_audio))
            audio_path = tmp.name
    else:
        return JSONResponse(status_code=400, content={"message": "Aucun fichier audio fourni."})

    langue_detectee = detect_language(texte_cible)
    transcription = transcribe_with_whisper(audio_path)
    score, erreurs, message = compare_texts(transcription, texte_cible)
    conseils = detect_pronunciation_tips(transcription, texte_cible, langue_detectee)
    audio_url = get_or_create_tts(texte_cible, langue_detectee)

    return AnalyseResult(
        moteur_utilise="whisper",
        langue_detectee=langue_detectee,
        transcription=transcription,
        attendu=texte_cible,
        score=score,
        erreurs=erreurs,
        message=message,
        audio_url=audio_url,
        conseils=conseils
    )

@app.post("/score")
async def score_only(fichier: UploadFile = File(...), texte_cible: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        content = await fichier.read()
        tmp.write(content)
        audio_path = tmp.name
    transcription = transcribe_with_whisper(audio_path)
    score, erreurs, message = compare_texts(transcription, texte_cible)
    return {"score": score, "message": message, "erreurs": erreurs}

@app.get("/exercice")
def exercice(langue: str, niveau: str):
    phrase = load_random_phrase(langue, niveau)
    audio_url = get_or_create_tts(phrase, langue)
    return {"phrase": phrase, "audio_url": audio_url}

@app.post("/ajouter-phrase")
async def ajouter_phrase(
    langue: str = Form(...),
    niveau: str = Form(...),
    phrase: str = Form(...)
):
    resultat = add_phrase(langue, niveau, phrase)
    return {"message": resultat}
