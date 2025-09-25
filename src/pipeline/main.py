from src.components.stt import STT
from src.components.llm_engine import LLMEngine
from src.components.tts import TTS

def run_pipeline():
    stt = STT()
    llm = LLMEngine()
    tts = TTS()

    audio, fs = stt.record(duration=10)
    text = stt.transcribe(audio, fs)
    print("👂 You said:", text)

    response = llm.query(text)
    print("🤖 LLM Response:", response)

    tts.speak(response)

if __name__ == "__main__":
    run_pipeline()
