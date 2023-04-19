#!/usr/bin/env python3
from pydub import AudioSegment
import openai
import sys
import os

openai.api_key = os.environ["OPENAPI_KEY"]

def transcribe_file(filename):
    transcript_filename = os.path.splitext(filename)[0] + '.txt'
    audio_file = AudioSegment.from_file(filename)

    chunk_size = 2 * 60 * 1000

    with open(transcript_filename, "w") as transcript:
        result = ''
        for i in range(0, len(audio_file), chunk_size):
            print("writing chunk:", i)
            chunk = audio_file[i:i+chunk_size]
            with chunk.export("/tmp/temp.wav", format="wav") as f:
                print("transcribing")
                result = openai.Audio.transcribe("whisper-1", f, prompt=result, response_format="text")
                transcript.write(result)
                transcript.flush()

if __name__ == '__main__':
    for fn in sys.argv[1:]:
        print("starting to transcribe file:", fn)
        transcribe_file(fn)
        print("file done")
