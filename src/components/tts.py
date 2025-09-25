import os
from elevenlabs import ElevenLabs
import torch
from transformers import pipeline
from config.settings import Settings

class TTS:
    def __init__(self):
        try:
            self.client = ElevenLabs(api_key=Settings.ELEVENLABS_API_KEY)
            self.voice = "Rachel"
            self.primary = True
        except Exception as e:
            print(f"⚠️ Falling back to Hugging Face TTS: {e}")
            self.tts = pipeline("text-to-speech", model="espnet/kan-bayashi-ljspeech")
            self.primary = False

    def speak(self, text: str):
        if self.primary:
            # CORRECTED: Use generate() instead of generate
            audio = self.client.generate(
                text=text, 
                voice=self.voice, 
                model="eleven_monolingual_v1"
            )
            with open("response.mp3", "wb") as f:
                f.write(audio)
            os.system("mpg123 response.mp3")
        else:
            audio = self.tts(text)["audio"]
            import soundfile as sf
            sf.write("response.wav", audio.numpy(), 22050)
            os.system("aplay response.wav")