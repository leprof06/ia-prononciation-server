import os
import urllib.request
import zipfile

# Dictionnaire des modèles Vosk disponibles (Dropbox)
vosk_models = {
    "cn": "https://www.dropbox.com/scl/fo/rjlas5gsop3ri9fj7ks0j/AJapDKFGxn-ZSB1vY2iP03k?rlkey=qa1uxx66ygkid85cbb0x782k8&st=ognq7vks&dl=1",
    "de": "https://www.dropbox.com/scl/fo/ofeesbrge29rpvcvxfm7i/AAtPiQewzmEAYQdXfddRrP8?rlkey=2fw54bx2mnnap1vjdpzllei2u&st=x4wx1zpm&dl=1",
    "en": "https://www.dropbox.com/scl/fo/f5n07mz2hco1scttgfz0v/AHp8lXdjyIvNCJK8QebEj88?rlkey=s1o2u9kxmiahfonwldjccdf2b&st=ysbmmvvf&dl=1",
    "es": "https://www.dropbox.com/scl/fo/vt86v45410a0gjo6rp13a/ADDRFYDId7_Rv19msR4xR00?rlkey=xm864h3d26rekg4m8jhv7jpl5&st=k6swut0i&dl=1",
    "fr": "https://www.dropbox.com/scl/fo/2feawxd2cxtltxr0td6nl/AFySa7zld62ggdq57GWenkk?rlkey=owlt6tyvyxv97jb45b2iw3o6n&st=kgdnns8o&dl=1",
    "ja": "https://www.dropbox.com/scl/fo/tktlwae3xzkj3icv4geki/AKgOzLAFd8YMIfdje3Py5_Q?rlkey=nftnwh5a3f05zka4vu7nyp0on&st=icfcc5pf&dl=1",
    "ko": "https://www.dropbox.com/scl/fo/76j3io9bbv9hjhuqi6vg4/AAMWSxjGEcO-K9dNPbinEy0?rlkey=j75wdvq9az4c7ok72pxrangfv&st=zet8ahf3&dl=1",
    "ru": "https://www.dropbox.com/scl/fo/8re3j5rty71ehmrux4dq3/ADCk7x9SVIwoO0ZxZf2c438?rlkey=ypu4ohejdygfzeei06oxjyw6q&st=805pqi2x&dl=1"
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
        zip_ref.extractall(dest_folder)

    os.remove(zip_path)
    print(f"Modèle {lang_code} prêt.")
