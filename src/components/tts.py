import sys, requests, tempfile, os, playsound
from src.core.logger import logging
from src.core.exception import CustomException
from src.config.config import ELEVENLABS_API_KEY

URL = "https://api.elevenlabs.io/v1/text-to-speech/exAVoiceId"  # you can replace with other voices

def speak_text(text: str):
    """Convert text to speech via ElevenLabs"""
    try:
        logging.info(f"[Zen bol raha hai]: {text}")
        resp = requests.post(
            URL,
            headers={
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_API_KEY,
            },
            json={"text": text, "voice_settings": {"stability": 0.7, "similarity_boost": 0.7}}
        )

        if resp.status_code != 200:
            logging.error(f"TTS error: {resp.text}")
            return

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp.write(resp.content)
        tmp.close()
        playsound.playsound(tmp.name)
        os.remove(tmp.name)

    except Exception as e:
        raise CustomException(e, sys)
