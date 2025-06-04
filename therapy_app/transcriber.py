import asyncio
from pathlib import Path
from typing import Any, Dict

import openai

from . import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


async def transcribe_audio(audio_path: Path) -> Dict[str, Any]:
    """Asynchronously transcribe audio using OpenAI Whisper API."""
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    async def _transcribe() -> Dict[str, Any]:
        with audio_path.open("rb") as f:
            try:
                result = openai.Audio.transcribe(
                    "whisper-1",
                    f,
                    response_format="verbose_json",
                    diarization="speaker",
                )
            except Exception as exc:
                raise RuntimeError(f"Transcription failed: {exc}") from exc
            return result

    return await asyncio.to_thread(_transcribe)


def save_transcript(result: Dict[str, Any], output_path: Path) -> None:
    output_path.write_text(str(result))
