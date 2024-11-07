# AI Sales Assistant Chatbot

### Evaluation Criteria

Your solution will be evaluated based on:

1. Reduction in overall latency (comparable to the "reference solution" above). Please share a demo video so we can easily evaluate.
2. Maintenance of conversation quality and realism (i.e the chatbot doesn't interrupt the human speaker while they're in the middle of speaking. The chatbot must say the same things that the reference solution would have said.)
3. Code quality and clarity of explanation in README.md

## Your Approach

Please describe your approach here.
Please also include a recorded video showing how fast your chatbot implementation is to respond.

### Approach

- **Bottle necks**: the sequential execution of OpenAI API request and ElevenLabs API request. the current workflow consists of

  - user says something
  - aai transcription starts
  - wait 500ms of silence
  - send transcript to openai, get response
  - send response to elevenlabs api for tts

- **current improvements to reduce latency**
  - _Streaming Response_: The response from the OpenAI API is now streamed, which allows for partial processing and quicker turnaround times.
  - _Asynchronous Audio Playback_: As responses are received incrementally from the OpenAI API, they are sent in real-time to the ElevenLabs API, and the audio playback begins simultaneously. This streaming mechanism cuts down on waiting times between the user's query and the system's verbal response.

### Video Demo

Please see this loom recording for a demo.

### Future Improvements

- faster API responses using Groq?
- streaming the OpenAI response texts to screen as chunks are received sequentially. Printing with `flush=True` lead to messy terminal outputs. need a better way of presenting this.
