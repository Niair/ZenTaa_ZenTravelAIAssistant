import sys
import os
from src.components.stt import STT
from src.components.llm_engine import LLMEngine
from src.components.tts import TTS

def test_stt():
    stt = STT()
    audio, fs = stt.record(duration=5)   # record 5 seconds for testing
    text = stt.transcribe(audio, fs)
    print("📝 STT Output:", text)

def test_llm():
    llm = LLMEngine()
    prompt = "Tell me a short fun fact about India."
    response = llm.query(prompt)
    print("🤖 LLM Response:", response)

def test_tts():
    tts = TTS()
    sample_text = "Hello Nihal! This is a test of the speech synthesis system."
    print("🔊 TTS Speaking...")
    tts.speak(sample_text)
    print("✅ TTS Finished.")

if __name__ == "__main__":
    print("=== TESTING STT ===")
    test_stt()
    print("\n=== TESTING LLM ===")
    test_llm()
    print("\n=== TESTING TTS ===")
    test_tts()
