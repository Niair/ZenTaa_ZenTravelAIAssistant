# test_sounddevice.py
import sounddevice as sd
print("Available audio devices:")
print(sd.query_devices())

# Test recording
import numpy as np
sample_rate = 16000
duration = 3  # seconds
print("Recording...")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
sd.wait()
print("Recording finished")
print(f"Recorded shape: {recording.shape}")