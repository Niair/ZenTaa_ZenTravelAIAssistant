import sys
from src.core.logger import logging
from src.core.exception import CustomException

def transcribe_audio(audio_file: str) -> str:
    """
    Convert speech audio into text.
    For Phase-1: returns a dummy text.
    Later: integrate Whisper, 11Labs, or Groq.
    """
    try:
        logging.info(f"Starting transcription for {audio_file}")
        # TODO: replace with real STT API
        text = "Hello Zen, mujhe Goa ka trip plan karna hai."
        logging.info(f"Transcription result: {text}")
        return text
    except Exception as e:
        logging.error("Error in STT module")
        raise CustomException(e, sys)
