# test/test_stt_vad.py
import sys
import os
import torch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from faster_whisper import WhisperModel
import tempfile
import wave
import sounddevice as sd
import numpy as np

def test_stt_without_vad():
    print("Testing STT without VAD (simple recording)...")
    
    # Initialize faster-whisper
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    model = WhisperModel("base", device=device, compute_type=compute_type)
    
    # Record 5 seconds of audio
    sample_rate = 16000
    duration = 5  # seconds
    
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        with wave.open(tmp_file.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            # Convert float32 to int16
            audio_data_int16 = (recording.flatten() * 32767).astype(np.int16)
            wf.writeframes(audio_data_int16.tobytes())
        
        # Transcribe
        segments, info = model.transcribe(tmp_file.name, beam_size=5)
        transcription = " ".join(segment.text for segment in segments)
        
        print(f"Detected language: {info.language}")
        print(f"Transcription: {transcription}")
    
    # Clean up
    try:
        os.unlink(tmp_file.name)
    except:
        pass

if __name__ == "__main__":
    test_stt_without_vad()