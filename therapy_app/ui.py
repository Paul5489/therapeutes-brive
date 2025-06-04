import asyncio
from pathlib import Path
from typing import Optional

from flask import Flask, request, jsonify, send_file

from .recorder import Recorder
from .transcriber import transcribe_audio, save_transcript
from .qa import load_transcript, ask_question, summarize_transcript

app = Flask(__name__)

PATIENTS_DIR = Path("patients")
PATIENTS_DIR.mkdir(exist_ok=True)


async def background_transcribe(audio_path: Path):
    result = await transcribe_audio(audio_path)
    save_transcript(result, audio_path.with_suffix(".json"))


@app.route("/record", methods=["POST"])
def record():
    patient = request.form.get("patient")
    duration = int(request.form.get("duration", 0))
    if not patient or duration <= 0:
        return jsonify({"error": "Invalid patient or duration"}), 400
    patient_dir = PATIENTS_DIR / patient
    recorder = Recorder(patient_dir)
    try:
        audio_path = recorder.start_recording(duration)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    asyncio.create_task(background_transcribe(audio_path))
    return jsonify({"message": "Recording finished", "audio": str(audio_path)})


@app.route("/transcript/<patient>/<date>")
def get_transcript(patient: str, date: str):
    transcript_path = PATIENTS_DIR / patient / date / "audio.json"
    if not transcript_path.exists():
        return jsonify({"error": "Transcript not found"}), 404
    return send_file(transcript_path)


@app.route("/ask", methods=["POST"])
def ask():
    transcript_path = Path(request.form.get("transcript"))
    question = request.form.get("question")
    if not question:
        return jsonify({"error": "Question required"}), 400
    try:
        transcript = load_transcript(transcript_path)
        answer = ask_question(transcript, question)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    return jsonify({"answer": answer})


@app.route("/summarize", methods=["POST"])
def summarize():
    transcript_path = Path(request.form.get("transcript"))
    try:
        transcript = load_transcript(transcript_path)
        summary = summarize_transcript(transcript)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    return jsonify({"summary": summary})


if __name__ == "__main__":
    app.run(debug=True)
