from src.core.logger import logger as logging
from src.core.exception import CustomException
from config import settings

from src.components.stt import get_stt_provider
from src.components.llm_engine import get_llm_provider
from src.components.tts import get_tts_provider

import sys
import os
from datetime import datetime

CONV_LOG = os.path.join(os.getcwd(), "logs", "conversations.log")
os.makedirs(os.path.dirname(CONV_LOG), exist_ok=True)

def append_conversation(user_text, assistant_text):
    with open(CONV_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | USER: {user_text}\n")
        f.write(f"{datetime.now().isoformat()} | ZEN : {assistant_text}\n\n")

def run_assistant():
    try:
        logging.info("Starting Zen (v3) CLI")
        stt = get_stt_provider()
        llm = get_llm_provider()
        tts = None
        try:
            from src.components.tts import get_tts_provider
            tts = get_tts_provider()
        except Exception as e:
            logging.warning("TTS provider init failed; fallback to pyttsx3")
            from src.components.tts import Pyttsx3TTS
            tts = Pyttsx3TTS()

        print("Zen ready. Speak when prompted (say 'exit' to quit).")
        while True:
            try:
                record_secs = settings.RECORD_SECONDS
                user_text = stt.transcribe_from_mic(record_seconds=record_secs)
            except TypeError:
                # some implementations may use different signature
                user_text = stt.transcribe_from_mic(record_secs)

            if not user_text:
                print("Kuch sunayi nahi diya, dobara boliye.")
                continue

            print("You:", user_text)
            if user_text.strip().lower() in ("exit", "quit", "stop"):
                farewell = "Thik hai dost, phir milte hain!"
                print("Zen:", farewell)
                tts.speak(farewell)
                break

            try:
                response = llm.generate(user_text)
            except Exception as e:
                logging.error("LLM error, sending fallback reply")
                response = "Maaf kijiye, abhi main thoda slow hoon. Dobara boliye."

            print("Zen:", response)
            append_conversation(user_text, response)

            try:
                tts.speak(response)
            except Exception as e:
                logging.error("TTS speak error, will print response instead")
                print("Zen (TTS failed):", response)

    except Exception as e:
        raise CustomException(e, sys)

if __name__ == "__main__":
    run_assistant()
