from src.components.stt import STT
from src.components.llm_engine import LLMEngine
from src.components.tts import TTS
import time

class ConversationalAgent:
    def __init__(self):
        print("🔄 Initializing ZenTravel AI Assistant...")
        self.stt = STT()
        self.llm = LLMEngine()
        self.tts = TTS()
        print("✅ All components initialized successfully!")
    
    def run_conversation(self, duration=5):
        """Run one conversation cycle: Listen → Process → Speak"""
        try:
            # Step 1: Listen (Speech-to-Text)
            print(f"🎙️ Recording for {duration} seconds...")
            audio, fs = self.stt.record(duration=duration)
            
            # Step 2: Transcribe
            print("📝 Transcribing...")
            user_text = self.stt.transcribe(audio, fs)
            print(f"👂 You said: {user_text}")
            
            if not user_text.strip():
                return "No speech detected"
            
            # Step 3: Generate response
            print("🤖 Thinking...")
            response = self.llm.query(user_text)
            print(f"💭 LLM Response: {response}")
            
            # Step 4: Speak (Text-to-Speech)
            print("🔊 Speaking...")
            self.tts.speak(response)
            
            return response
            
        except Exception as e:
            print(f"❌ Error in conversation: {e}")
            return f"Error: {e}"

def run_pipeline():
    agent = ConversationalAgent()
    
    print("\n" + "="*50)
    print("🎯 ZenTravel AI Assistant - Conversation Test")
    print("="*50)
    print("Speak after the 'Recording...' message")
    print("Press Ctrl+C to exit")
    print("="*50)
    
    try:
        while True:
            response = agent.run_conversation(duration=5)
            print(f"\n💬 Response: {response}")
            print("-" * 30)
            time.sleep(1)  # Small pause between conversations
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    run_pipeline()