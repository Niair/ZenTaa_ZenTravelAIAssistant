import os
from dotenv import load_dotenv

load_dotenv()  # loads .env in project root

STT_PROVIDER = os.getenv("STT_PROVIDER", "deepgram").lower()
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "huggingface").lower()
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "elevenlabs").lower()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

RECORD_SECONDS = int(os.getenv("RECORD_SECONDS", "5"))
