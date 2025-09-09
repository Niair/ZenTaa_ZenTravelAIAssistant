import sys, requests
from src.core.logger import logging
from src.core.exception import CustomException
from src.config.config import HF_API_KEY

HF_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def get_response(user_input: str) -> str:
    """Get smart reply from HuggingFace"""
    try:
        logging.info(f"LLM input: {user_input}")
        resp = requests.post(HF_URL, headers=HEADERS, json={"inputs": user_input})
        data = resp.json()
        logging.info(f"Raw LLM: {data}")

        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        elif isinstance(data, dict) and "error" in data:
            return f"LLM error: {data['error']}"
        return "Sorry, mujhe samajh nahi aaya 🤔"
    except Exception as e:
        raise CustomException(e, sys)
