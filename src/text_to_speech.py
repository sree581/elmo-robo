import os
from elevenlabs.client import ElevenLabs
import tempfile
import playsound

def speak(text):
    api_key = os.getenv("ELEVEN_API_KEY")

    if not api_key:
        print("❌ ElevenLabs API key not found.")
        return

    client = ElevenLabs(api_key=api_key)

    audio_stream = client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM",
        model_id="eleven_turbo_v2",

        text=text
    )

    # Collect generator into bytes
    audio_bytes = b"".join(audio_stream)

    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file.write(audio_bytes)
    temp_file.close()

    playsound.playsound(temp_file.name)
