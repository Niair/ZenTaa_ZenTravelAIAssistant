import requests, sys, tempfile, sounddevice as sd, wave
from src.core.logger import logging
from src.core.exception import CustomException
from src.config.config import ASSEMBLYAI_API_KEY

ASSEMBLY_URL = "https://api.assemblyai.com/v2"

def record_audio(duration=5, samplerate=16000):
    """Record audio from mic and save to temp wav"""
    try:
        logging.info("🎤 Recording from mic...")
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
        sd.wait()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio.tobytes())
        return tmp.name
    except Exception as e:
        raise CustomException(e, sys)

def transcribe_from_mic():
    """Send recorded audio to AssemblyAI and return text"""
    try:
        wav_path = record_audio()
        headers = {"authorization": ASSEMBLYAI_API_KEY}

        # Upload file
        with open(wav_path, "rb") as f:
            upload = requests.post(f"{ASSEMBLY_URL}/upload", headers=headers, data=f)
        audio_url = upload.json()["upload_url"]

        # Request transcript
        resp = requests.post(f"{ASSEMBLY_URL}/transcript", headers=headers, json={"audio_url": audio_url})
        transcript_id = resp.json()["id"]

        # Poll with timeout
        import time
        start = time.time()
        while True:
            r = requests.get(f"{ASSEMBLY_URL}/transcript/{transcript_id}", headers=headers)
            data = r.json()
            status = data.get("status")

            print(f"⏳ Status: {status}")  # 👈 progress feedback

            if status == "completed":
                text = data.get("text", "")
                logging.info(f"📝 Transcribed: {text}")
                return text
            elif status == "error":
                raise Exception(f"AssemblyAI error: {data}")
            
            if time.time() - start > 60:   # 👈 1-minute timeout
                raise Exception("Timeout: Transcription took too long")

            time.sleep(3)  # wait before next poll

    except Exception as e:
        raise CustomException(e, sys)
