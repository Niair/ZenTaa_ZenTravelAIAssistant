import requests
import json
import os

def text_to_speech_elevenlabs(api_key, text, voice_id, filename="output.mp3"):
    """Direct API call to ElevenLabs"""
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Audio saved as {filename}")
        os.system(f"start {filename}")  # Windows
        # os.system(f"open {filename}")  # Mac
        # os.system(f"xdg-open {filename}")  # Linux
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Usage
api_key = "sk_1fa1f8dcf428f90830ae533190b7d8e6901670c01e3c3a82"
text = "How are you Zen? कैसा है यार तू?"
voice_id = "JBFqnCBsd6RMkjVDRZzb"

text_to_speech_elevenlabs(api_key, text, voice_id)