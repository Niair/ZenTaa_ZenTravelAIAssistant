import os
from config.settings import Settings

class TTS:
    def __init__(self):
        self.primary = None

        # Try TTSOpenAI first (your actual service)
        try:
            from openai import OpenAI
            # Point to TTSOpenAI's API endpoint
            self.ttsopenai_client = OpenAI(
                api_key=Settings.TTSOPENAI_API_KEY,  # You'll need to add this to settings
                base_url="https://api.ttsopenai.com/v1"  # TTSOpenAI's endpoint
            )
            self.primary = "ttsopenai"
            print("✅ Using TTSOpenAI for TTS")
        except Exception as e:
            print(f"⚠️ TTSOpenAI not available: {e}")

        # Fallback to ElevenLabs
        if not self.primary:
            try:
                from elevenlabs.client import ElevenLabs
                self.eleven = ElevenLabs(api_key=Settings.ELEVENLABS_API_KEY)
                self.voice_id = "21m00Tcm4TlvDq8ikWAM"
                self.model_id = "eleven_multilingual_v2"
                self.primary = "elevenlabs"
                print("✅ Using ElevenLabs as fallback")
            except Exception as e:
                print(f"⚠️ ElevenLabs not available: {e}")

        # Last fallback → Hugging Face
        if not self.primary:
            try:
                from transformers import pipeline
                self.tts = pipeline("text-to-speech", model="espnet/kan-bayashi-ljspeech")
                self.primary = "huggingface"
                print("✅ Using Hugging Face TTS as fallback")
            except Exception as e:
                print(f"❌ No TTS services available: {e}")

    def speak(self, text: str):
        if self.primary == "ttsopenai":
            # TTSOpenAI API call (adjust based on their specific API)
            response = self.ttsopenai_client.audio.speech.create(
                model="tts-1",  # Check TTSOpenAI's available models
                voice="alloy",  # Check available voices
                input=text
            )
            audio_bytes = response.read()
            with open("response.mp3", "wb") as f:
                f.write(audio_bytes)
            os.system("start response.mp3")

        elif self.primary == "elevenlabs":
            response = self.eleven.text_to_speech.convert(
                text=text,
                voice_id=self.voice_id,
                model_id=self.model_id,
                output_format="mp3_44100_128",
            )
            audio_bytes = b"".join(response)
            with open("response.mp3", "wb") as f:
                f.write(audio_bytes)
            os.system("start response.mp3")

        elif self.primary == "huggingface":
            audio = self.tts(text)["audio"]
            import soundfile as sf
            sf.write("response.wav", audio.numpy(), 22050)
            os.system("start response.wav")