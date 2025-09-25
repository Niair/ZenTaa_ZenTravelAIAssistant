import sounddevice as sd
import numpy as np
from groq import Groq
from faster_whisper import WhisperModel
from config.settings import Settings

class STT:
    def __init__(self):
        self.client = Groq(api_key=Settings.GROQ_API_KEY)
        try:
            # Test Groq Whisper
            self.model = "whisper-large-v3"
            self.primary = True
        except Exception as e:
            print("⚠️ Falling back to Faster-Whisper:", e)
            self.model = WhisperModel("medium")
            self.primary = False

    def record(self, duration=10, fs=16000):
        print("🎙️ Recording...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()
        return audio.flatten(), fs

    def transcribe(self, audio, fs=16000):
        if self.primary:
            with open("temp.wav", "wb") as f:
                import soundfile as sf
                sf.write(f, audio, fs)
            resp = self.client.audio.transcriptions.create(
                file=open("temp.wav", "rb"),
                model=self.model,
                language="hi"
            )
            return resp.text
        else:
            text, info = self.model.transcribe(audio, beam_size=5, language="hi")
            # Optional Urdu → Hindi remap
            if info.language == "ur":
                info.language = "hi"
            return text

