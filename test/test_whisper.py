# test_whisper_basic.py
from faster_whisper import WhisperModel

# Try a simple test without recording
model = WhisperModel("base", device="cpu", compute_type="int8")
print("Model loaded successfully")

# You can test with a sample audio file if you have one
# segments, info = model.transcribe("sample_audio.wav", beam_size=5)
# print(f"Detected language: {info.language}")


# run>> python test/test_whisper.py