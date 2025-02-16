import soundfile as sf
import wave
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AudioProcessor:
    def __init__(self):
        self.buffer = []
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def process_chunk(self, audio_chunk):
        webm_audio = io.BytesIO(audio_chunk) # in-memory webm audio
        audio_segment = AudioSegment.from_file(webm_audio, format="webm")
        self.buffer.append(audio_segment)

    async def transcribe_latest(self):
        if len(self.buffer) == 0:
            return None
        latest_segment = self.buffer[-1]
        transcription = await self.groq_client.audio.transcriptions.create(
            file=latest_segment, # Required audio file
            model="distil-whisper-large-v3-en", # Required model to use for transcription
            prompt="Specify context or spelling",  # Optional
            response_format="json",  # Optional
            language="en",  # Optional
            temperature=0.0  # Optional
        )
        print("[DEBUG]", f"Transcription: {transcription.text}")
        return transcription.text
                
    def get_full_audio(self):
        joined_bytes = b"".join(self.buffer)

        file_name = "full_audio.wav"

        with open(file_name, "wb") as f:
            f.write(joined_bytes)

        return file_name


