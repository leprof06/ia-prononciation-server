import whisper

model = whisper.load_model("base")

def transcribe_with_whisper(audio_path: str) -> str:
    result = model.transcribe(audio_path, language=None)
    return result.get("text", "").strip()
