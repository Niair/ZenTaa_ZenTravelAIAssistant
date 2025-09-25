import sys
import os
from src.components.stt import STT
from src.components.llm_engine import LLMEngine
# from src.components.tts import TTS  # Comment out the broken version
from src.components.fixed_tts import TTS  # Use the fixed version instead


def test_stt():
    """Test Speech-to-Text functionality"""
    print("🎙️ Testing Speech-to-Text (STT)...")
    stt = STT()
    print("🔴 Recording for 5 seconds - please speak now...")
    audio, fs = stt.record(duration=5)   # record 5 seconds for testing
    print("⏹️ Recording stopped. Processing...")
    text = stt.transcribe(audio, fs)
    print(f"📝 STT Output: {text}")
    return text


def test_llm():
    """Test Large Language Model with travel-related prompts"""
    print("🤖 Testing Travel AI Assistant (LLM)...")
    llm = LLMEngine()
    
    # FIXED: Use travel-related prompts instead of random facts
    travel_prompts = [
        "I want to visit India for 7 days. What are the top 3 destinations you recommend?",
        "What should I pack for a trip to India in monsoon season?",
        "How can I plan a budget trip to Rajasthan?"
    ]
    
    # Test with a travel-related prompt
    prompt = travel_prompts[0]  # Use the first travel prompt
    print(f"💬 Prompt: {prompt}")
    
    response = llm.query(prompt)
    print(f"🤖 LLM Response: {response}")
    
    # Verify the response is travel-related
    travel_keywords = ['travel', 'trip', 'visit', 'destination', 'india', 'places', 'tourism']
    response_lower = response.lower()
    is_travel_related = any(keyword in response_lower for keyword in travel_keywords)
    
    if is_travel_related:
        print("✅ LLM is responding appropriately to travel queries!")
    else:
        print("⚠️ LLM response doesn't seem travel-related. Check your system prompt.")
    
    return response


def test_tts():
    """Test Text-to-Speech functionality with fixed implementation"""
    print("🔊 Testing Text-to-Speech (TTS)...")
    tts = TTS()
    
    # Travel-themed test message
    sample_text = "Hello! I'm your Zen Travel AI Assistant. I'm ready to help you plan amazing trips to India and beyond. How can I assist you today?"
    print(f"📢 TTS Speaking: '{sample_text}'")
    
    try:
        tts.speak(sample_text)
        print("✅ TTS completed successfully!")
    except Exception as e:
        print(f"❌ TTS failed: {e}")


def full_integration_test():
    """Test the full STT -> LLM -> TTS pipeline"""
    print("\n" + "="*50)
    print("🔄 FULL INTEGRATION TEST")
    print("="*50)
    
    # Step 1: Get speech input
    print("1️⃣ Listening for your travel question...")
    stt = STT()
    audio, fs = stt.record(duration=5)
    user_input = stt.transcribe(audio, fs)
    print(f"   Heard: {user_input}")
    
    # Step 2: Process with LLM
    print("2️⃣ Processing with Travel AI...")
    llm = LLMEngine()
    # Add travel context to the input
    travel_prompt = f"As a helpful travel assistant for India, please respond to: {user_input}"
    ai_response = llm.query(travel_prompt)
    print(f"   AI Response: {ai_response[:100]}...")
    
    # Step 3: Speak the response
    print("3️⃣ Speaking the response...")
    tts = TTS()
    tts.speak(ai_response)
    
    print("✅ Full integration test completed!")


if __name__ == "__main__":
    print("🚀 ZEN TRAVEL AI ASSISTANT - COMPONENT TESTING")
    print("=" * 60)
    
    # Individual component tests
    print("\n=== TESTING STT ===")
    test_stt()
    
    print("\n=== TESTING LLM (Travel-Focused) ===")
    test_llm()
    
    print("\n=== TESTING TTS (Fixed Version) ===")
    test_tts()
    
    # Optional: Full integration test
    print("\n" + "="*60)
    user_choice = input("🤔 Run full integration test (STT->LLM->TTS)? (y/n): ")
    if user_choice.lower() == 'y':
        full_integration_test()
    
    print("\n✅ All tests completed!")
    print("💡 If TTS still fails, make sure your ElevenLabs API key is properly set in config/settings.py")
    print("💡 For LLM context, consider adding a system prompt about being a travel assistant")