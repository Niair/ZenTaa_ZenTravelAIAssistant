import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
