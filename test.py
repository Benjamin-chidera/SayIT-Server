from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os

openai = OpenAI( 
                # base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("OPENAI_API_KEY"),)

speech_file_path = Path(__file__).parent / "speech.mp3"
with openai.audio.speech.with_streaming_response.create(
  model="gpt-4o-mini-tts",
  voice="alloy",
  input="The quick brown fox jumped over the lazy dog.",
) as response:
  response.stream_to_file(speech_file_path)
