import os
from elevenlabs.client import ElevenLabs  # Updated import
from elevenlabs.play import play          # For playing audio
import torch
from transformers import pipeline
from config.settings import Settings


class TTS:
    def __init__(self):
        try:
            # Updated initialization with proper client import
            self.client = ElevenLabs(api_key=Settings.ELEVENLABS_API_KEY)
            # Use voice_id instead of voice name for better compatibility
            self.voice_id = "EXAVITQu4vr4xnSDxMaL"  # Default voice ID (Sarah)
            # Alternative voice IDs you can try:
            # "JBFqnCBsd6RMkjVDRZzb" - George (male)
            # "21m00Tcm4TlvDq8ikWAM" - Rachel (female)
            # "AZnzlk1XvdvUeBnXmlld" - Domi (female)
            self.primary = True
            print("✅ ElevenLabs TTS initialized successfully")
        except Exception as e:
            print(f"⚠️ ElevenLabs failed: {e}")
            print("⚠️ Falling back to Hugging Face TTS")
            self.tts = pipeline("text-to-speech", model="espnet/kan-bayashi-ljspeech")
            self.primary = False

    def speak(self, text: str):
        if self.primary:
            try:
                # NEW METHOD: Use text_to_speech.convert instead of generate
                audio = self.client.text_to_speech.convert(
                    text=text,
                    voice_id=self.voice_id,
                    model_id="eleven_multilingual_v2",  # Updated model
                    output_format="mp3_44100_128"
                )
                
                # Save audio to file
                with open("response.mp3", "wb") as f:
                    for chunk in audio:
                        f.write(chunk)
                
                # Play the audio file
                os.system("mpg123 response.mp3")  # Linux/Mac
                # os.system("start response.mp3")  # Windows alternative
                
            except Exception as e:
                print(f"❌ ElevenLabs TTS failed: {e}")
                print("🔄 Falling back to Hugging Face TTS")
                self._fallback_tts(text)
        else:
            self._fallback_tts(text)
    
    def _fallback_tts(self, text: str):
        """Fallback TTS using Hugging Face"""
        try:
            audio = self.tts(text)["audio"]
            import soundfile as sf
            sf.write("response.wav", audio.numpy(), 22050)
            os.system("aplay response.wav")  # Linux
            # os.system("start response.wav")  # Windows alternative
        except Exception as e:
            print(f"❌ Fallback TTS also failed: {e}")

    def list_available_voices(self):
        """Helper method to list available voices"""
        if self.primary:
            try:
                voices = self.client.voices.search()
                print("🎙️ Available voices:")
                for voice in voices.voices[:10]:  # Show first 10 voices
                    print(f"   • {voice.name} (ID: {voice.voice_id})")
                return voices.voices
            except Exception as e:
                print(f"❌ Could not fetch voices: {e}")
                return []
        return []


# Test the fixed TTS
if __name__ == "__main__":
    print("=== TESTING FIXED TTS ===")
    tts = TTS()
    
    # List available voices
    tts.list_available_voices()
    
    # Test speech
    sample_text = "Hello! I'm your Zen Travel AI Assistant. How can I help you plan your perfect trip today?"
    print(f"🔊 Speaking: {sample_text}")
    tts.speak(sample_text)
    print("✅ TTS test completed!")