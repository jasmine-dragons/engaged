import os
import io
from typing import List, Optional
from dotenv import load_dotenv
from pydub import AudioSegment
from groq import Groq

# Load environment variables
load_dotenv()

class AudioProcessor:
    def __init__(self):
        """Initialize the audio processor"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY in environment variables.")
        
        self.groq_client = Groq(api_key=api_key)
        self.combined_audio: bytes = b''  # Store continuously concatenated audio

    def process_chunk(self, chunk: bytes):
        """Process an incoming audio chunk"""
        if chunk:
            # Continuously concatenate chunks to maintain WebM structure
            if not self.combined_audio:
                self.combined_audio = chunk  # First chunk contains header
            else:
                self.combined_audio += chunk

    async def transcribe_latest(self) -> Optional[str]:
        """Transcribe the latest audio chunk"""
        if not self.combined_audio:
            return None
        
        try:
            print("[DEBUG] Transcribing audio...")
            # Create a file-like object from the combined audio
            audio_file = io.BytesIO(self.combined_audio)
            audio_file.name = "audio.webm"  # Required for format recognition

            print("[DEBUG] Sending to Groq...")

            # Transcribe using the WAV bytes
            transcription = self.groq_client.audio.transcriptions.create(
                file=("audio.webm", audio_file),
                model="distil-whisper-large-v3-en",
                prompt="Transcribe the following audio. If you cannot understand the audio, respond with 'I'm sorry, I could not understand the audio.'",
                response_format="json",
                language="en",
                temperature=0.0
            )

            print("[DEBUG] Transcription:", transcription.text)
            return transcription.text

        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None

    def get_full_audio(self) -> Optional[bytes]:
        """Get the full concatenated audio"""
        if not self.combined_audio:
            return None
            
        try:
            # Convert the combined WebM to WAV
            audio_file = io.BytesIO(self.combined_audio)
            audio_file.name = "audio.webm"
            
            audio_segment = AudioSegment.from_file(audio_file, format="webm")
            wav_buffer = io.BytesIO()
            audio_segment.export(wav_buffer, format="wav")
            wav_buffer.seek(0)
            return wav_buffer.read()
            
        except Exception as e:
            print(f"Error converting audio: {e}")
            return None

    def clear_buffer(self):
        """Clear all audio buffers"""
        self.combined_audio = b''
