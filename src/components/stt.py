import sys
import tempfile
import wave
import time
import requests
import sounddevice as sd
from src.core.logger import logger as logging
from src.core.exception import CustomException
from config import settings

# Deepgram: simple REST single-shot endpoint (good for short snippets)
# AssemblyAI used as fallback if DEEPGRAM unavailable

class BaseSTT:
    def transcribe_from_mic(self, record_seconds: int):
        raise NotImplementedError

class DeepgramSTT(BaseSTT):
    def __init__(self, api_key=None):
        self.api_key = api_key or settings.DEEPGRAM_API_KEY
        if not self.api_key:
            raise ValueError("DEEPGRAM_API_KEY not set in .env")

    def record(self, duration, samplerate=16000):
        try:
            logging.info("Recording audio from mic...")
            audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
            sd.wait()
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            with wave.open(tmp.name, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(samplerate)
                wf.writeframes(audio.tobytes())
            logging.info(f"Saved temp audio: {tmp.name}")
            return tmp.name
        except Exception as e:
            logging.error("Recording failed")
            raise CustomException(e, sys)

    def transcribe_from_mic(self, record_seconds):
        try:
            wav_path = self.record(record_seconds)
            with open(wav_path, "rb") as f:
                headers = {"Authorization": f"Token {self.api_key}", "Content-Type": "audio/wav"}
                # Deepgram's 'listen' endpoint returns JSON transcript synchronously for small files
                resp = requests.post("https://api.deepgram.com/v1/listen?model=general&language=hi-IN", headers=headers, data=f)
            data = resp.json()
            logging.info(f"Deepgram raw response: {data}")
            # Deepgram response contains 'results' -> channels[0] -> alternatives[0] -> transcript
            transcript = ""
            try:
                transcript = data["results"]["channels"][0]["alternatives"][0].get("transcript", "")
            except Exception:
                transcript = data.get("transcript") or ""
            return transcript.strip()
        except Exception as e:
            logging.error("Deepgram transcription failed")
            raise CustomException(e, sys)

class AssemblyAI_STT(BaseSTT):
    def __init__(self, api_key=None):
        self.api_key = api_key or settings.ASSEMBLYAI_API_KEY
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY not set in .env")
        self.base = "https://api.assemblyai.com/v2"

    def record(self, duration, samplerate=16000):
        try:
            logging.info("Recording audio from mic...")
            audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
            sd.wait()
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            with wave.open(tmp.name, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(samplerate)
                wf.writeframes(audio.tobytes())
            logging.info(f"Saved temp audio: {tmp.name}")
            return tmp.name
        except Exception as e:
            logging.error("Recording failed")
            raise CustomException(e, sys)

    def upload(self, file_path):
        try:
            headers = {"authorization": self.api_key}
            with open(file_path, "rb") as f:
                r = requests.post(f"{self.base}/upload", headers=headers, data=f)
            r.raise_for_status()
            return r.json()["upload_url"]
        except Exception as e:
            logging.error("AssemblyAI upload failed")
            raise CustomException(e, sys)

    def transcribe_from_mic(self, record_seconds, timeout=60):
        try:
            wav_path = self.record(record_seconds)
            audio_url = self.upload(wav_path)
            headers = {"authorization": self.api_key, "content-type": "application/json"}
            r = requests.post(f"{self.base}/transcript", headers=headers, json={"audio_url": audio_url})
            r.raise_for_status()
            transcript_id = r.json()["id"]
            start = time.time()
            while True:
                r = requests.get(f"{self.base}/transcript/{transcript_id}", headers=headers)
                r.raise_for_status()
                data = r.json()
                status = data.get("status")
                logging.info(f"AssemblyAI status: {status}")
                if status == "completed":
                    return data.get("text", "").strip()
                if status == "error":
                    raise Exception(f"AssemblyAI error: {data}")
                if time.time() - start > timeout:
                    raise Exception("AssemblyAI transcription timeout")
                time.sleep(1)
        except Exception as e:
            logging.error("AssemblyAI transcription failed")
            raise CustomException(e, sys)


def get_stt_provider():
    prov = settings.STT_PROVIDER
    if prov == "deepgram":
        try:
            return DeepgramSTT()
        except Exception as e:
            logging.warning("Deepgram init failed; falling back to AssemblyAI")
            return AssemblyAI_STT()
    elif prov == "assemblyai":
        return AssemblyAI_STT()
    else:
        raise ValueError(f"Unknown STT provider: {prov}")
