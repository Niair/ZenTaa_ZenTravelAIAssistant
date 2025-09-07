from src.components.stt import transcribe_audio
from src.components.tts import speak_text
from src.components.llm_engine import get_response
from src.core.logger import logging
from src.core.exception import CustomException
import sys

def run_assistant():
    """
    Main loop for Zen Assistant (Phase-1).
    Controlled conversation with 'exit' command to stop.
    """
    try:
        logging.info("Zen Assistant Started - Phase-1")

        while True:
            # For Phase-1 testing, take text input instead of real audio
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit", "stop"]:
                speak_text("Thik hai dost! Fir milte hain 👋")
                logging.info("Zen Assistant Stopped by User")
                break

            # Get response from LLM
            response = get_response(user_input)

            # Speak response
            print(f"Zen: {response}")
            speak_text(response)

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    run_assistant()
