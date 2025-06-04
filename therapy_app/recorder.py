import os
import wave
from datetime import datetime
from pathlib import Path
from typing import Optional

import sounddevice as sd
from scipy.io.wavfile import write


class Recorder:
    def __init__(self, patient_dir: Path, samplerate: int = 44100):
        self.patient_dir = patient_dir
        self.samplerate = samplerate
        self.recording = None

    def start_recording(self, duration: int) -> Path:
        """Record audio for a given duration in seconds."""
        if duration <= 0:
            raise ValueError("Duration must be positive")
        date_dir = self.patient_dir / datetime.now().strftime('%Y-%m-%d')
        date_dir.mkdir(parents=True, exist_ok=True)
        audio_path = date_dir / 'audio.wav'
        try:
            self.recording = sd.rec(int(duration * self.samplerate), samplerate=self.samplerate, channels=1)
            sd.wait()
            write(audio_path, self.samplerate, self.recording)
        except Exception as exc:
            raise RuntimeError(f"Failed to record audio: {exc}") from exc
        return audio_path

    def is_recording(self) -> bool:
        return self.recording is not None
