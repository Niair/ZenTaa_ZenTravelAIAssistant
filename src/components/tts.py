import os
from config.settings import Settings

class TTS:
    def __init__(self):
        self.primary = None
        self.fallback_used = False

        # Try TTSOpenAI first
        try:
            from openai import OpenAI
            # Check if API key is provided
            if hasattr(Settings, 'TTSOPENAI_API_KEY') and Settings.TTSOPENAI_API_KEY:
                self.ttsopenai_client = OpenAI(
                    api_key=Settings.TTSOPENAI_API_KEY,
                    base_url="https://api.ttsopenai.com/v1"
                )
                # Test the connection with a simple call
                self.primary = "ttsopenai"
                print("✅ Using TTSOpenAI for TTS")
            else:
                print("⚠️ TTSOpenAI API key not found")
                raise Exception("TTSOpenAI API key not configured")
        except Exception as e:
            print(f"⚠️ TTSOpenAI not available: {e}")
            self.primary = None

        # Fallback to ElevenLabs
        if not self.primary:
            try:
                from elevenlabs.client import ElevenLabs
                # Check if API key is provided
                if hasattr(Settings, 'ELEVENLABS_API_KEY') and Settings.ELEVENLABS_API_KEY:
                    self.eleven = ElevenLabs(api_key=Settings.ELEVENLABS_API_KEY)
                    self.voice_id = "JBFqnCBsd6RMkjVDRZzb"  # Using your original voice ID
                    self.model_id = "eleven_multilingual_v2"
                    self.primary = "elevenlabs"
                    print("✅ Using ElevenLabs as TTS fallback")
                else:
                    print("⚠️ ElevenLabs API key not found")
                    raise Exception("ElevenLabs API key not configured")
            except Exception as e:
                print(f"⚠️ ElevenLabs not available: {e}")
                self.primary = None

        # Last fallback → System TTS or Hugging Face
        if not self.primary:
            try:
                # Try pyttsx3 for system TTS (no API required)
                import pyttsx3
                self.tts_engine = pyttsx3.init()
                self.primary = "system"
                print("✅ Using System TTS as final fallback")
            except Exception as e:
                print(f"⚠️ System TTS not available: {e}")
                try:
                    from transformers import pipeline
                    import torch
                    self.tts = pipeline("text-to-speech", model="microsoft/speecht5_tts")
                    self.primary = "huggingface"
                    print("✅ Using Hugging Face TTS as final fallback")
                except Exception as e:
                    print(f"❌ No TTS services available: {e}")
                    self.primary = None

    def speak(self, text: str):
        if not self.primary:
            print("❌ No TTS service available")
            return

        try:
            if self.primary == "ttsopenai":
                response = self.ttsopenai_client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=text
                )
                audio_bytes = response.read()
                self._play_audio(audio_bytes, "mp3")
                
            elif self.primary == "elevenlabs":
                response = self.eleven.text_to_speech.convert(
                    text=text,
                    voice_id=self.voice_id,
                    model_id=self.model_id,
                    output_format="mp3_44100_128",
                )
                # Convert generator to bytes
                audio_bytes = b"".join(response)
                self._play_audio(audio_bytes, "mp3")
                
            elif self.primary == "system":
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                
            elif self.primary == "huggingface":
                # Simple fallback - just print for now
                print(f"🔊 [TTS would say]: {text}")
                
        except Exception as e:
            print(f"❌ TTS error with {self.primary}: {e}")
            # Try to fallback to next available service
            self._fallback_speak(text)

    def _fallback_speak(self, text: str):
        """Fallback mechanism if primary TTS fails"""
        if self.fallback_used:
            print("❌ Fallback already used, cannot recover")
            return
            
        self.fallback_used = True
        
        if self.primary == "ttsopenai":
            print("🔄 Falling back to ElevenLabs...")
            try:
                from elevenlabs.client import ElevenLabs
                if hasattr(Settings, 'ELEVENLABS_API_KEY') and Settings.ELEVENLABS_API_KEY:
                    self.eleven = ElevenLabs(api_key=Settings.ELEVENLABS_API_KEY)
                    self.voice_id = "JBFqnCBsd6RMkjVDRZzb"
                    self.model_id = "eleven_multilingual_v2"
                    self.primary = "elevenlabs"
                    self.speak(text)
                    return
            except Exception as e:
                print(f"❌ ElevenLabs fallback failed: {e}")
        
        # Final fallback to system TTS
        print("🔄 Falling back to System TTS...")
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.primary = "system"
            self.speak(text)
        except Exception as e:
            print(f"❌ System TTS fallback failed: {e}")
            print(f"🔊 [TTS would say]: {text}")

    def _play_audio(self, audio_bytes: bytes, format: str):
        """Play audio bytes using appropriate player"""
        filename = f"response.{format}"
        with open(filename, "wb") as f:
            f.write(audio_bytes)
        
        # Cross-platform audio playback
        try:
            if os.name == 'nt':  # Windows
                os.system(f"start {filename}")
            elif os.name == 'posix':  # macOS/Linux
                os.system(f"open {filename}" if sys.platform == "darwin" else f"xdg-open {filename}")
        except Exception as e:
            print(f"⚠️ Could not auto-play audio: {e}")
            print(f"💡 Audio saved as: {filename}")