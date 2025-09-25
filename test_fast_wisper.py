from faster_whisper import WhisperModel

def transcribe_hinglish_working():
    model = WhisperModel("small", device="cpu")
    
    # 👇 This is the key: Treat it as English but don't translate meaning
    segments, info = model.transcribe(
        "test.wav",
        beam_size=5,
        task="transcribe",
        language="en",  # Force English alphabet
        temperature=0.0,  # More deterministic
        best_of=5,
        # Add a prompt that encourages phonetic transcription
        initial_prompt="Transcribe the Hindi speech using English letters phonetically"
    )
    
    print("Detected language:", info.language)
    
    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

transcribe_hinglish_working()