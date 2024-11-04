# Notes for project

## Bottle Necks

- CANNOT change to use different APIs
- CANNOT change the 500ms wait on silence

## Potential Improvements

- stream response from OpenAI API
- start playing audio as the response streams

## Things to check

- async streaming of OpenAI API
  - do streaming always do a word at a time? might have to do post processing if stream tokens instead of words
- does elevenlabs tts api support streaming response?
  - if not, considering requests per output word but that might be too slow.
