import os
import assemblyai as aai
from packages.elevenlabs_tts import speak  # Update the class name if different
from packages.sales_chatbot import SalesChatbot

from dotenv import load_dotenv

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
            self.respond(transcript.text)
        else:
            print("[User]: " + transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        return


    def on_close(self):
        return
    
    def respond(self, transcript):

        self.stop_transcription()

        # generate response from OpenAI
        response = self.chatbot.generate_response(transcript)

        print("[Bot]: ", response)

        # speak response using ElevenLabs
        speak(response)
        
        self.start_transcription()

voice_bot = VoiceBot()
voice_bot.start_transcription()