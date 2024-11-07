# Notes for project

## Bottle Necks

- CANNOT change to use different APIs
- CANNOT change the 500ms wait on silence

## Current Flow

- user says something
- aai transcription starts
- wait 500ms of silence
- send transcript to openai, get response
- send response to elevenlabs api for tts

## Potential Improvements

- stream response from OpenAI API
- start playing audio as the response streams

## Things to check

- async streaming of OpenAI API
  - do streaming always do a word at a time? might have to do post processing if stream tokens instead of words
- does elevenlabs tts api support streaming response?
  - if not, considering requests per output word but that might be too slow.

## Debugging

- tried to follow the tutorial [here](https://github.com/elevenlabs/elevenlabs-python?tab=readme-ov-file#input-streaming), but the synchronous operations didn't _really_ allow for streaming while getting data back from the websocket endpoint.
- followed [this](https://elevenlabs.io/docs/api-reference/websockets#example-voice-streaming-using-elevenlabs-and-openai) section instead. got the streaming to work, now need to make other functions async too in `main.py` and `sales_chatbot.py`
- also learned that `print` is a blocking operation. I still want users to see what's being generated on the screen, but cannot use print for this.
- the first bit of audio kinda gets cut off each time?
