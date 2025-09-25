import sounddevice as sd
import soundfile as sf

duration = 5
samplerate = 16000
print("🎤 Recording...")
audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
sd.wait()
sf.write("test.wav", audio, samplerate)
print("✅ Saved test.wav")