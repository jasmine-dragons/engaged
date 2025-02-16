from cmd import PROMPT
import os
from groq import Groq
from dotenv import load_dotenv
import subprocess

load_dotenv()

class AudioProcessor:
    def __init__(self):
        self.buffer = []  # Store raw audio chunks
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.chunk_count = 0

    def process_chunk(self, audio_chunk):
        """Store a raw audio chunk"""
        # Save chunk to a temporary file
        chunk_filename = f"temp_chunk_{self.chunk_count}.webm"
        with open(chunk_filename, 'wb') as f:
            f.write(audio_chunk)
        self.buffer.append(chunk_filename)
        self.chunk_count += 1

    async def transcribe_latest(self):
        """Transcribe the latest audio chunk"""
        if len(self.buffer) == 0:
            return None
            
        # Get the latest chunk filename
        latest_chunk = self.buffer[-1]
        
        try:
            # Transcribe using the chunk file
            with open(latest_chunk, "rb") as f:
                transcription = self.groq_client.audio.transcriptions.create(
                    file=(latest_chunk, f.read()),
                    model="distil-whisper-large-v3-en",
                    prompt="Transcribe the following audio. If you cannot understand the audio, respond with 'I'm sorry, I could not understand the audio.'",
                    response_format="json",
                    language="en",
                    temperature=0.0
                )
            return transcription.text
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None

    def get_full_audio(self, output_path="full_audio.webm"):
        """Combine all audio chunks using ffmpeg"""
        if not self.buffer:
            return None
            
        try:
            # Create a file listing all chunks
            concat_file = "concat_list.txt"
            with open(concat_file, 'w') as f:
                for chunk_file in self.buffer:
                    f.write(f"file '{chunk_file}'\n")
            
            # Use ffmpeg to concatenate the chunks
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_file,
                '-c', 'copy',  # Copy without re-encoding
                '-y',  # Overwrite output file
                output_path
            ]
            
            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            if process.returncode != 0:
                print(f"FFmpeg error: {process.stderr.decode()}")
                return None
                
            return output_path
            
        except Exception as e:
            print(f"Error combining audio chunks: {e}")
            return None
            
        finally:
            # Clean up temporary files
            if os.path.exists(concat_file):
                os.remove(concat_file)
            for chunk_file in self.buffer:
                if os.path.exists(chunk_file):
                    os.remove(chunk_file)
            self.buffer = []
            self.chunk_count = 0