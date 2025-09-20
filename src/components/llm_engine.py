import sys
import requests
from src.core.logger import logger as logging
from src.core.exception import CustomException
from config import settings

class BaseLLM:
    def generate(self, user_input: str) -> str:
        raise NotImplementedError

class HuggingFaceLLM(BaseLLM):
    def __init__(self, api_key=None, model="google/flan-t5-large"):
        self.api_key = api_key or settings.HF_API_KEY
        self.model = model
        if not self.api_key:
            raise ValueError("HF_API_KEY not set in .env")
        self.url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def generate(self, user_input: str, max_tokens=128):
        try:
            prompt = f"Reply in Hinglish, friendly conversational style. Keep replies short and helpful.\nUser: {user_input}\nZen:"
            logging.info(f"Sending to HF: {prompt[:200]}...")
            resp = requests.post(self.url, headers=self.headers, json={"inputs": prompt, "parameters": {"max_new_tokens": max_tokens}}, timeout=60)
            data = resp.json()
            logging.info(f"HuggingFace raw response: {data}")
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"].strip()
            if isinstance(data, dict) and "error" in data:
                return f"LLM error: {data['error']}"
            return "Sorry, mujhe samajh nahi aaya."
        except Exception as e:
            logging.error("HuggingFace LLM call failed")
            raise CustomException(e, sys)

class CohereLLM(BaseLLM):
    def __init__(self, api_key=None):
        self.api_key = api_key or settings.COHERE_API_KEY
        if not self.api_key:
            raise ValueError("COHERE_API_KEY not set in .env")
        self.url = "https://api.cohere.ai/generate"
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def generate(self, user_input: str, max_tokens=128):
        try:
            prompt = f"Reply in Hinglish, friendly conversational style. User: {user_input}"
            logging.info("Sending to Cohere...")
            resp = requests.post(self.url, headers=self.headers, json={"prompt": prompt, "max_tokens": max_tokens})
            data = resp.json()
            logging.info(f"Cohere raw response: {data}")
            if "generations" in data and len(data["generations"]) > 0:
                return data["generations"][0]["text"].strip()
            return "Sorry, mujhe samajh nahi aaya."
        except Exception as e:
            logging.error("Cohere LLM call failed")
            raise CustomException(e, sys)

def get_llm_provider():
    prov = settings.LLM_PROVIDER
    if prov == "huggingface":
        return HuggingFaceLLM()
    elif prov == "cohere":
        return CohereLLM()
    else:
        logging.warning("Unknown LLM provider, defaulting to HuggingFace")
        return HuggingFaceLLM()
