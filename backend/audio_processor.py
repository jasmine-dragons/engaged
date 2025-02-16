import soundfile as sf
import wave
import os
from groq import Groq
from dotenv import load_dotenv
import io
from pydub import AudioSegment

load_dotenv()

class AudioProcessor:
    def __init__(self):
        self.buffer = []  # Store AudioSegment objects
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def process_chunk(self, audio_chunk):
        """Process a WebM audio chunk and store it"""
        webm_audio = io.BytesIO(audio_chunk)
        audio_segment = AudioSegment.from_file(webm_audio, format="webm")
        self.buffer.append(audio_segment)

    async def transcribe_latest(self):
        """Transcribe the latest audio segment"""
        if len(self.buffer) == 0:
            return None
            
        latest_segment = self.buffer[-1]
        # Export latest segment to temporary file for transcription
        temp_file = "temp_latest.wav"
        latest_segment.export(temp_file, format="wav")
        
        try:
            with open(temp_file, "rb") as f:
                transcription = await self.groq_client.audio.transcriptions.create(
                    file=(temp_file, f.read()),
                    model="distil-whisper-large-v3-en",
                    response_format="json",
                    language="en",
                    temperature=0.0
                )
            return transcription.text
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def get_full_audio(self, output_path="full_audio.wav"):
        """Combine all audio segments and save to WAV file"""
        if not self.buffer:
            return None
            
        # Concatenate all audio segments
        combined = sum(self.buffer[1:], self.buffer[0])
        # Export to WAV file
        combined.export(output_path, format="wav")
        return output_path