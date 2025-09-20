# <stt.py>

import sounddevice as sd
import numpy as np
import torch
import collections
import sys
import logging
import tempfile
import wave
import os
from src.core.exception import CustomException
from config import settings

# --- Silero VAD Setup ---
try:
    model, utils = torch.hub.load(
        repo_or_dir='snakers4/silero-vad',
        model='silero_vad',
        force_reload=False,
        onnx=False
    )
    (get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils
except Exception as e:
    logging.error(f"Failed to load Silero VAD model: {e}")
    model = None

# --- Faster Whisper Setup ---
faster_whisper_model = None
if settings.STT_PROVIDER == "faster_whisper":
    try:
        from faster_whisper import WhisperModel
        device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"
        faster_whisper_model = WhisperModel(
            settings.WHISPER_MODEL_SIZE, 
            device=device, 
            compute_type=compute_type
        )
        logging.info(f"Loaded faster-whisper model on {device}")
    except Exception as e:
        logging.error(f"Failed to load faster-whisper model: {e}")
        faster_whisper_model = None

def record_until_silence(
    sample_rate=16000,
    chunk_size=512,  # Fixed to 512 as required by VAD
    padding_ms=800,
    speech_threshold=0.4
):
    """
    Record audio from the microphone until a period of silence is detected
    using the Silero VAD model.
    """
    if model is None:
        raise CustomException("Silero VAD model is not loaded. Cannot record.", sys)

    num_padding_chunks = int(padding_ms / 1000 * sample_rate / chunk_size)

    ring_buffer = collections.deque(maxlen=num_padding_chunks)
    triggered = False
    voiced_chunks = []

    logging.info("🎤 Listening... Speak now!")

    # Create a VAD iterator for more efficient processing
    vad_iterator = VADIterator(model)
    
    with sd.InputStream(samplerate=sample_rate, blocksize=chunk_size,
                        dtype='float32', channels=1) as stream:
        while True:
            # Read a chunk of audio data from the microphone
            audio_chunk_np, overflowed = stream.read(chunk_size)
            if overflowed:
                logging.warning("Audio buffer overflowed!")

            # Convert numpy array to a torch tensor
            audio_chunk_tensor = torch.from_numpy(audio_chunk_np[:, 0])

            # Use VAD iterator for speech probability
            speech_dict = vad_iterator(audio_chunk_tensor, return_seconds=True)
            is_speech = speech_dict is not None

            if not triggered:
                ring_buffer.append((audio_chunk_tensor, is_speech))
                num_voiced = len([chunk for chunk, speech in ring_buffer if speech])

                # If enough speech frames are in the buffer, trigger recording
                if num_voiced > 0.8 * ring_buffer.maxlen:
                    triggered = True
                    logging.info("🎙️ Speech detected...")
                    # Dump the buffer to start the recording
                    for chunk, s in ring_buffer:
                        voiced_chunks.append(chunk)
                    ring_buffer.clear()
            else:
                # We are actively recording
                voiced_chunks.append(audio_chunk_tensor)
                ring_buffer.append((audio_chunk_tensor, is_speech))
                num_unvoiced = len([chunk for chunk, speech in ring_buffer if not speech])

                # If the buffer is full of silence, stop recording
                if num_unvoiced > 0.9 * ring_buffer.maxlen:
                    logging.info("🛑 Silence detected. Stopping recording.")
                    break

    # Reset the VAD iterator
    vad_iterator.reset()
    
    # Concatenate all recorded chunks into a single tensor
    if not voiced_chunks:
        logging.warning("No speech detected.")
        return None

    full_recording_tensor = torch.cat(voiced_chunks)
    return full_recording_tensor.numpy()

class FasterWhisperProvider:
    @staticmethod
    def transcribe_from_mic(*args, **kwargs):
        """
        Records audio and transcribes it using faster-whisper.
        """
        try:
            if faster_whisper_model is None:
                raise CustomException("Faster-whisper model is not loaded.", sys)
                
            # Record audio using VAD
            audio_data = record_until_silence()
            
            if audio_data is None:
                return ""
                
            # Save audio to a temporary file for faster-whisper
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                with wave.open(tmp_file.name, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)  # 16-bit
                    wf.setframerate(16000)
                    # Convert float32 to int16
                    audio_data_int16 = (audio_data * 32767).astype(np.int16)
                    wf.writeframes(audio_data_int16.tobytes())
                
                # Transcribe using faster-whisper
                segments, info = faster_whisper_model.transcribe(
                    tmp_file.name, 
                    beam_size=5,
                    language=settings.WHISPER_LANGUAGE if hasattr(settings, 'WHISPER_LANGUAGE') else None
                )
            
            # Combine all segments into a single text
            transcription = " ".join(segment.text for segment in segments)
            
            logging.info(f"Detected language: {info.language} with probability {info.language_probability}")
            return transcription
            
        except Exception as e:
            raise CustomException(e, sys)
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_file.name)
            except:
                pass

def get_stt_provider():
    if settings.STT_PROVIDER == "faster_whisper":
        return FasterWhisperProvider()
    else:
        # Default to faster-whisper
        return FasterWhisperProvider()

# Add this at the end of stt.py
if __name__ == "__main__":
    # Simple test when run directly
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("Testing STT module directly...")
    stt = get_stt_provider()
    print("Please speak for 5 seconds after the message...")
    text = stt.transcribe_from_mic(record_seconds=5)
    print(f"Transcribed text: {text}")