import os
import urllib.request
import zipfile

# Dictionnaire des modèles Vosk à télécharger
vosk_models = {
    "fr": "https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip",
    "en": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
    "de": "https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip",
    "es": "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip",
    "ru": "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip",
    "ja": "https://alphacephei.com/vosk/models/vosk-model-small-ja-0.22.zip",
    "zh": "https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip",
    "ko": "https://alphacephei.com/vosk/models/vosk-model-small-ko-0.22.zip"
}

models_dir = "models"
os.makedirs(models_dir, exist_ok=True)

def download_and_extract(lang_code, url):
    dest_folder = os.path.join(models_dir, f"vosk-{lang_code}")
    if os.path.exists(dest_folder):
        print(f"Modèle déjà présent pour {lang_code}, saut.")
        return

    zip_path = f"{models_dir}/vosk-{lang_code}.zip"
    print(f"Téléchargement du modèle {lang_code}...")
    urllib.request.urlretrieve(url, zip_path)

    print(f"Décompression du modèle {lang_code}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(models_dir)

    # Renommer le dossier extrait
    extracted_dir = [d for d in os.listdir(models_dir) if d.startswith("vosk-model") and os.path.isdir(os.path.join(models_dir, d))][-1]
    os.rename(os.path.join(models_dir, extracted_dir), dest_folder)
    os.remove(zip_path)
    print(f"Modèle {lang_code} prêt.")

for code, url in vosk_models.items():
    download_and_extract(code, url)

print("✅ Tous les modèles nécessaires sont prêts.")
