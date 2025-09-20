import sys
import tempfile
import os
import requests
import playsound
from src.core.logger import logger as logging
from src.core.exception import CustomException
from config import settings
import pyttsx3

class ElevenLabsTTS:
    def __init__(self, api_key=None, voice_id=None):
        self.api_key = api_key or settings.ELEVENLABS_API_KEY
        self.voice_id = voice_id or settings.ELEVENLABS_VOICE_ID
        if not self.api_key or not self.voice_id:
            raise ValueError("ElevenLabs API key or voice id not set in .env")

    def speak(self, text: str):
        try:
            logging.info(f"ElevenLabs TTS speaking: {text[:120]}...")
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": self.api_key}
            data = {"text": text, "voice_settings": {"stability": 0.6, "similarity_boost": 0.6}}
            r = requests.post(url, headers=headers, json=data, timeout=60)
            r.raise_for_status()
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tmp.write(r.content)
            tmp.close()
            playsound.playsound(tmp.name)
            os.remove(tmp.name)
        except Exception as e:
            logging.error("ElevenLabs TTS failed")
            raise CustomException(e, sys)

class Pyttsx3TTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)

    def speak(self, text: str):
        try:
            logging.info(f"pyttsx3 speaking: {text[:120]}...")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logging.error("pyttsx3 TTS failed")
            raise CustomException(e, sys)

def get_tts_provider():
    prov = settings.TTS_PROVIDER
    if prov == "elevenlabs":
        try:
            return ElevenLabsTTS()
        except Exception as e:
            logging.warning("ElevenLabs init failed, falling back to pyttsx3")
            return Pyttsx3TTS()
    elif prov == "pyttsx3":
        return Pyttsx3TTS()
    else:
        logging.warning("Unknown TTS provider, defaulting to ElevenLabs")
        try:
            return ElevenLabsTTS()
        except Exception:
            return Pyttsx3TTS()
