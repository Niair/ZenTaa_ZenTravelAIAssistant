import sys
from src.core.logger import logging
from src.core.exception import CustomException

def speak_text(text: str):
    """
    Convert text to speech.
    For Phase-1: prints to console.
    Later: integrate gTTS, 11Labs, or Groq TTS.
    """
    try:
        logging.info(f"TTS speaking: {text}")
        print(f"[Zen bol raha hai]: {text}")  # Hinglish style
    except Exception as e:
        logging.error("Error in TTS module")
        raise CustomException(e, sys)
