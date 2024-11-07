import os
from dotenv import load_dotenv
from elevenlabs import play
from elevenlabs.client import ElevenLabs, AsyncElevenLabs
# Load environment variables
load_dotenv(override=True)
from typing import AsyncGenerator
# Get API key from environment
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
import time
ELEVENLABS_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # Default voice, you can change this


client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
aclient = AsyncElevenLabs(api_key=ELEVENLABS_API_KEY)
async def speak(text: str) -> float:
    try:
        audio = await aclient.generate(
            text=text,
            voice=ELEVENLABS_VOICE_ID,
            model="eleven_monolingual_v1",
            stream=True, 
        )
        listen_task = asyncio.create_task(stream(audio))
        return await listen_task


    except Exception as e:
        print(f"Error in text-to-speech: {str(e)}")
        raise e

import asyncio
import websockets
import json
import base64
import shutil
import os
import subprocess

# Set OpenAI API key
def is_installed(lib_name: str) -> bool:
    return shutil.which(lib_name) is not None

# async version of the stream function at elevenlabs.stream
async def stream(audio_stream):
    """Stream audio data using mpv player."""
    if not is_installed("mpv"):
        raise ValueError(
            "mpv not found, necessary to stream audio. "
            "Install instructions: https://mpv.io/installation/"
        )

    mpv_process = subprocess.Popen(
        ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    timestamp = None
    first_chunk = True
    async for chunk in audio_stream:
        if chunk:
            mpv_process.stdin.write(chunk)
            mpv_process.stdin.flush()
            if first_chunk:
                print("Started streaming audio", flush=True)
                timestamp = time.time()
                first_chunk = False
    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()
    return timestamp


# async version of the text_chunker function as elevenlabs.realtime_tts.text_chunker
async def text_chunker(chunks: AsyncGenerator[str, None]):
    """Split text into chunks, ensuring to not break sentences."""
    splitters = (".", ",", "?", "!", ";", ":", "—", "-", "(", ")", "[", "]", "}", " ")
    buffer = ""

    async for text in chunks:
        if not text:
            continue
        if buffer.endswith(splitters):
            yield buffer + " "
            buffer = text
        elif text.startswith(splitters):
            yield buffer + text[0] + " "
            buffer = text[1:]
        else:
            buffer += text

    if buffer:
        yield buffer + " "

async def text_to_speech_input_streaming(text_iterator: AsyncGenerator[str, None], voice_id: str = ELEVENLABS_VOICE_ID):
    """Send text to ElevenLabs API and stream the returned audio."""
    uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id=eleven_turbo_v2_5"

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "text": " ",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
            "xi_api_key": ELEVENLABS_API_KEY,
        }))

        async def listen():
            """Listen to the websocket for audio data and stream it."""
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    if data.get("audio"):
                        yield base64.b64decode(data["audio"])
                    elif data.get('isFinal'):
                        break
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed")
                    break

        listen_task = asyncio.create_task(stream(listen()))

        async for text in text_chunker(text_iterator):
            await websocket.send(json.dumps({"text": text}))

        await websocket.send(json.dumps({"text": ""}))

        return await listen_task
