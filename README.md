# therapeutes-brive

Outil pour enregistrer, transcrire et analyser des séances de thérapie.

## Installation

1. Créez un environnement virtuel et activez‑le.
2. Installez les dépendances :

```bash
pip install flask sounddevice scipy openai python-dotenv
```

3. Copiez `.env.example` vers `.env` et renseignez votre clé OpenAI.

## Fichier `.env`

```
OPENAI_API_KEY=sk-...
```

## Utilisation

Les données des patients sont organisées dans le dossier `patients/<nom>/<date>/`.
Chaque enregistrement audio est sauvegardé sous `audio.wav` et la transcription
au format JSON sous `audio.json`.

Pour lancer l'interface Flask :

```bash
python -m therapy_app.ui
```

Via l'API vous pouvez démarrer un enregistrement, consulter la transcription,
obtenir un résumé ou poser des questions à GPT.

En mode hors‑ligne (sans clé OpenAI) vous pouvez toujours enregistrer les
fichiers audio puis les transcrire plus tard.
