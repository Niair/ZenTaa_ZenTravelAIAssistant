# download_models.py
import os
from huggingface_hub import snapshot_download, login
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_API_KEY")
if hf_token:
    login(token=hf_token)

models = [
    ("speechbrain/asr-whisper-large-v2-commonvoice-hi", "./models/whisper-hi"),
    ("openai/whisper-large-v3",               "./models/whisper-large-v3"),
]

for repo, path in models:
    os.makedirs(path, exist_ok=True)
    snapshot_download(repo_id=repo, local_dir=path, token=None)
