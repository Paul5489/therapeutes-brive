from pathlib import Path
from typing import List

import openai

from . import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def load_transcript(transcript_path: Path) -> str:
    if not transcript_path.exists():
        raise FileNotFoundError(f"Transcript not found: {transcript_path}")
    return transcript_path.read_text()


def ask_question(transcript: str, question: str) -> str:
    prompt = (
        "You are a helpful assistant for therapists. "
        "Answer the question based on the transcript provided.\n\n" + transcript + "\n\nQuestion: " + question
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message["content"].strip()
    except Exception as exc:
        raise RuntimeError(f"GPT query failed: {exc}") from exc


def summarize_transcript(transcript: str) -> str:
    prompt = (
        "Summarize the following therapy session transcript succinctly:"\
        f"\n\n{transcript}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message["content"].strip()
    except Exception as exc:
        raise RuntimeError(f"GPT summarization failed: {exc}") from exc
