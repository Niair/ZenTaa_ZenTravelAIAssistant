# src/components/openai_stt.py
from openai import OpenAI
import sounddevice as sd
import numpy as np
import io
import tempfile
import wave
from dotenv import load_dotenv
import os

load_dotenv()

class OpenAISTT:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        print("✅ OpenAI STT Ready (v1.0+)")

    def record_and_transcribe(self, duration=15):
        print(f"🎙️ Recording for {duration} seconds...")
        audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='float32')
        sd.wait()
        print("✅ Recording finished")
        
        # Save to temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            with wave.open(tmp_file.name, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(16000)
                wav_file.writeframes((audio * 32767).astype(np.int16).tobytes())
            
            print("📝 Transcribing with OpenAI Whisper API...")
            
            # New v1.0+ API syntax
            with open(tmp_file.name, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="hi",  # Hindi
                    response_format="text"
                )
            
            # Clean up temporary file
            os.unlink(tmp_file.name)
            
            print(f"👉 Result: {transcript}")
            return transcript

# Usage
if __name__ == "__main__":
    try:
        stt = OpenAISTT()
        result = stt.record_and_transcribe(duration=20)
        print(f"🎉 Final transcription: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure OPENAI_API_KEY is set in your .env file")
