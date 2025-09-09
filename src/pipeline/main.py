from src.components.stt import transcribe_from_mic
from src.components.tts import speak_text
from src.components.llm_engine import get_response
from src.core.logger import logging
from src.core.exception import CustomException
import sys

def run_assistant():
    logging.info("🚀 Zen Assistant Phase-2 started")
    try:
        while True:
            text = transcribe_from_mic()
            if text.lower() in ["exit","quit","stop"]:
                speak_text("Thik hai dosto, phir milte hain! 👋")
                break
            reply = get_response(text)
            speak_text(reply)
    except Exception as e:
        raise CustomException(e, sys)

if __name__ == "__main__":
    run_assistant()
