# IA Prononciation Server

Un serveur FastAPI permettant d'analyser la prononciation d'un enregistrement audio en comparant avec une phrase cible. Ce projet est intégré à un GPT personnalisé de type professeur de langues, conçu pour aider à l'apprentissage de la prononciation dans de nombreuses langues.

## Fonctionnalités

- Détection automatique de la langue (via `langdetect`)
- Transcription avec Whisper
- Comparaison de la transcription avec la phrase attendue
- Calcul d’un score de prononciation
- Suggestions personnalisées pour améliorer la prononciation
- Génération audio du texte cible avec TTS
- API REST extensible (exercices, retour vocal, etc.)
- Génération automatique des fichiers d'exercice si non existants

## API disponible

### POST `/analyse-prononciation`
Analyse la prononciation d’un fichier audio comparé à une phrase cible.

**Champs attendus :**

- `fichier` : fichier audio (.wav, .mp3, .m4a, etc.)
- `texte_cible` : texte attendu
- `base64_audio` (en option) : alternative au fichier, encodé en base64

### GET `/health`
Retourne `{"status": "ok"}` si le serveur est opérationnel.

### POST `/score`
Retourne uniquement le score de prononciation, sans les conseils.

### GET `/exercice?langue=fr&niveau=A2`
Renvoie une phrase aléatoire et son audio associé.

---

## Installation locale

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
Politique de confidentialité
Ce projet ne collecte ni n’enregistre aucune donnée personnelle. Les fichiers audio soumis sont temporairement utilisés pour le traitement de la prononciation et ne sont pas conservés après l’analyse. Le serveur est hébergé sur Render et suit leur politique de gestion de données.

En utilisant cette API via un GPT personnalisé, vous acceptez implicitement la politique de confidentialité décrite ici :
👉 https://www.support-learn-with-yann.com/politique-confidentialite

Auteurs
Ce projet a été créé par Yann Martinez dans le cadre de ses outils pédagogiques pour l’apprentissage des langues.
Vous pouvez retrouver ses autres services sur :
🌐 https://www.support-learn-with-yann.com