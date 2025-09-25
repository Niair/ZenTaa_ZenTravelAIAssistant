from elevenlabs.client import ElevenLabs
from config.settings import Settings

client = ElevenLabs(api_key=Settings.ELEVENLABS_API_KEY)

voices = client.voices.get_all()

for v in voices.voices:
    print(f"Name: {v.name}, ID: {v.voice_id}")
