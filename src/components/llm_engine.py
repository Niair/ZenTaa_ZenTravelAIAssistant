import sys
import random
from src.core.logger import logging
from src.core.exception import CustomException

def get_response(user_input: str) -> str:
    """
    Generate a response from the assistant.
    For Phase-1: simple hardcoded Hinglish replies (random).
    Later: plug into OpenAI / Groq / other LLM.
    """
    try:
        logging.info(f"LLM received input: {user_input}")
        text = user_input.lower()

        if "japan" in text:
            response = "Japan waah! Cherry blossoms aur sushi try karna bhoolna mat 🌸🍣"
        elif "goa" in text:
            response = "Goa mast jagah hai doston! Beaches aur party mood ON 🏖️"
        elif "manali" in text:
            response = "Manali ke pahad aur thandi hawa… perfect getaway 🏔️"
        elif "hello" in text or "hi" in text or 'or kesa hai' in text:
            response = "Arre hello doston! Main Zen hoon, tera travel dost 🤝"
        else:
            response = "Samajh gaya! Travel ke sapne hamesha acche lagte hain 😎"

        logging.info(f"LLM response: {response}")
        return response

    except Exception as e:
        logging.error("Error in LLM engine")
        raise CustomException(e, sys)
