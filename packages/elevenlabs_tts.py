import os
from dotenv import load_dotenv
from elevenlabs import play, stream
from elevenlabs.client import ElevenLabs

# Load environment variables
load_dotenv(override=True)

# Get API key from environment
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

ELEVENLABS_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # Default voice, you can change this

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def speak(text_gen):
    try:
        # audio = client.generate(
        #     text=text,
        #     voice=ELEVENLABS_VOICE_ID,
        #     model="eleven_monolingual_v1"
        # )
        audio_stream = client.generate(
            text=text_gen,
            voice=ELEVENLABS_VOICE_ID,
            model="eleven_multilingual_v2",
            stream=True
        )
        stream(audio_stream)
    except Exception as e:
        print(f"Error in text-to-speech: {str(e)}")
        raise e