# src/components/stt_working.py
import torch
from transformers import pipeline
import sounddevice as sd
import numpy as np
import gc
import warnings

# Suppress warnings for clean output
warnings.filterwarnings("ignore")

class WorkingSTT:
    def __init__(self):
        print("🚀 Loading Whisper Large V3 (Fixed Version)...")
        
        # Use pipeline which handles token limits automatically
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-large-v3",
            device=0 if torch.cuda.is_available() else -1,
            dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            chunk_length_s=10,
            return_timestamps=False
        )
        
        print("✅ Ready for Hindi/English/Hinglish transcription (100% FREE)")

    def record_audio(self, duration=20):
        """Record audio from microphone"""
        print(f"🎙️ Recording for {duration} seconds...")
        print("💡 Speak naturally in Hindi, English, or mix both!")
        
        audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='float32')
        sd.wait()
        print("✅ Recording finished!")
        
        # Normalize audio
        audio = audio.flatten()
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio)) * 0.95
        
        return audio

    def transcribe_audio(self, audio, lang=None):
        """Improved transcription with optional language forcing"""
        print("📝 Transcribing...")

        try:
            if lang:
                result = self.pipe(
                    {"array": audio, "sampling_rate": 16000},
                    language=lang,
                    max_new_tokens=200,
                    temperature=0.0
                )
            else:
                result = self.pipe(
                    {"array": audio, "sampling_rate": 16000},
                    max_new_tokens=200,
                    temperature=0.0
                )

            text = result["text"].strip()
            return text

        except Exception as e:
            print(f"❌ Transcription failed: {e}")
            return ""

        

    def transcribe_chunks(self, audio, chunk_duration=25):
        """Transcribe long audio in smaller chunks"""
        chunk_samples = chunk_duration * 16000
        results = []
        total_chunks = (len(audio) + chunk_samples - 1) // chunk_samples
        
        print(f"📊 Processing {total_chunks} chunks of {chunk_duration}s each...")
        
        for i in range(0, len(audio), chunk_samples):
            chunk_num = i // chunk_samples + 1
            chunk = audio[i:i+chunk_samples]
            
            if len(chunk) > 8000:  # Skip very short chunks (< 0.5s)
                print(f"🔄 Processing chunk {chunk_num}/{total_chunks}...")
                result = self.transcribe_audio(chunk)
                if result:
                    results.append(result)
                    print(f"👉 Chunk {chunk_num}: {result}")
                else:
                    print(f"⏭️ Chunk {chunk_num}: silent or failed")
        
        return " ".join(results)

    def record_and_transcribe(self, duration=20):
        """Complete workflow: record and transcribe"""
        # Record audio
        audio = self.record_audio(duration)
        
        # Choose transcription method based on duration
        if duration > 30:
            print("📊 Using chunked transcription for long audio...")
            final_text = self.transcribe_chunks(audio)
        else:
            print("📝 Using single transcription...")
            final_text = self.transcribe_audio(audio)
        
        # Post-process result
        if final_text:
            # Clean up common issues
            final_text = final_text.replace("  ", " ").strip()
            
            # Basic Hinglish corrections
            corrections = {
                "मैं को": "मुझे",
                "में को": "मुझे",
                "है को": "है जो",
                "आप को": "आपको"
            }
            
            for wrong, correct in corrections.items():
                final_text = final_text.replace(wrong, correct)
            
            print(f"\n🎉 FINAL TRANSCRIPTION:")
            print(f"📝 {final_text}")
            
            # Save to file
            try:
                with open("transcription.txt", "w", encoding="utf-8") as f:
                    f.write(final_text)
                print(f"💾 Saved to transcription.txt")
            except:
                pass
                
        else:
            print(f"\n⚠️ No transcription generated")
            print("💡 Try:")
            print("   - Speaking louder/clearer")
            print("   - Moving closer to microphone")
            print("   - Reducing background noise")
        
        return final_text

    def test_microphone(self):
        """Test if microphone is working"""
        print("🎤 Testing microphone for 3 seconds...")
        test_audio = sd.rec(int(3 * 16000), samplerate=16000, channels=1, dtype='float32')
        sd.wait()
        
        volume = np.max(np.abs(test_audio))
        print(f"🔊 Audio level: {volume:.3f}")
        
        if volume > 0.01:
            print("✅ Microphone is working!")
            return True
        else:
            print("❌ Microphone seems quiet - check your settings")
            return False

# Main usage
if __name__ == "__main__":
    try:
        print("🎯 FREE Local Hindi/English STT System (Fixed)")
        print("=" * 60)
        
        # Initialize STT
        stt = WorkingSTT()
        
        # Test microphone first
        print("\n🧪 Testing microphone...")
        stt.test_microphone()
        
        print("\n" + "=" * 60)
        print("🎤 Ready to transcribe! Press Ctrl+C to stop anytime")
        print("=" * 60)
        
        # Record and transcribe
        result = stt.record_and_transcribe(duration=15)  # Reduced to 15s for reliability
        
        if result:
            print(f"\n✅ SUCCESS! Transcription completed.")
        else:
            print(f"\n❌ No result - please try again with clearer audio")
        
    except KeyboardInterrupt:
        print("\n\n👋 Stopped by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
