import os
import assemblyai as aai
from packages.elevenlabs_tts import speak, text_to_speech_input_streaming  # Update the class name if different
from packages.sales_chatbot import SalesChatbot
import asyncio
from dotenv import load_dotenv
import time
load_dotenv(override=True)

class VoiceBot:

    def __init__(self):
        aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.transcriber = None
        self.chatbot = SalesChatbot()
            
    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate = 16000,
            on_data = self.on_data,
            on_error = self.on_error,
            on_open = self.on_open,
            on_close = self.on_close,
            end_utterance_silence_threshold = 500
        )

        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate =16000)
        self.transcriber.stream(microphone_stream)
    
    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        print("Session ID:", session_opened.session_id)
        return


    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            print("[User]: " + transcript.text, end="\n")            
            asyncio.run(self.respond_stream(transcript.text))


        else:
            print("[User]: " + transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        return

    def on_close(self):
        return
    
    async def respond(self, transcript: str):
        """
            This is the original respond method with 
            slight modifications to make it async.
        """
        start_time = time.time()

        self.stop_transcription()
        # generate response from OpenAI
        response = self.chatbot.generate_response(transcript)
        # speak response using ElevenLabs
        end_time = await speak(response)
        print("[Bot]: ", response)
        duration = end_time - start_time
        print(f"latency: {duration}", flush=True)
        self.start_transcription()
    async def respond_stream(self, transcript: str):
        """
        
            This is the optimized approach to achieve lower latency.
            
            We first get an async generator from openai's api that
            streams the response, and send that generator directly to 
            the Elevenlab's websocket api for tts generation.

            The latency measured is the time from this function being invoked
            to the audio starting to play.
        
        """
        start_time = time.time()

        self.stop_transcription()

        response_generator = self.chatbot.generate_response_stream(transcript)
        end_time = await text_to_speech_input_streaming(response_generator)
        if not end_time:
            raise RuntimeError()
        duration = end_time - start_time
        print(f"time to start talking: {duration}")
        self.start_transcription()

if __name__ == "__main__":
    voice_bot = VoiceBot()
    try:
        voice_bot.start_transcription()
    except KeyboardInterrupt:
        print("Interrupted by user. Shutting down...")
        voice_bot.stop_transcription()