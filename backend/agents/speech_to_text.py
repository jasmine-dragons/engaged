import asyncio
from typing import Callable, Awaitable, Optional
import websockets
import json
import base64
from deepgram import Deepgram
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SpeechToTextManager:
    def __init__(self, on_text_callback: Callable[[str], Awaitable[None]]):
        """
        Initialize the speech to text manager
        on_text_callback: async function that will be called when speech is converted to text
        """
        self.on_text_callback = on_text_callback
        self.deepgram = Deepgram(os.getenv("DEEPGRAM_API_KEY"))
        self.deepgram_socket: Optional[websockets.WebSocketClientProtocol] = None
        self.is_listening = False
        
        # Configure Deepgram parameters
        self.deepgram_params = {
            "smart_format": True,
            "model": "nova-2",
            "language": "en",
            "punctuate": True,
            "interim_results": False,
            "endpointing": True,  # Enable voice activity detection
        }

    async def handle_audio_stream(self, audio_data: bytes):
        """Handle incoming audio data from Zoom"""
        if self.deepgram_socket and self.is_listening:
            try:
                # Send audio data to Deepgram
                await self.deepgram_socket.send(audio_data)
            except Exception as e:
                print(f"Error sending audio to Deepgram: {str(e)}")

    async def _handle_deepgram_message(self, message: str):
        """Handle messages received from Deepgram"""
        try:
            response = json.loads(message)
            if response.get("type") == "Results":
                # Extract the transcribed text
                transcript = response["channel"]["alternatives"][0]["transcript"]
                if transcript.strip():  # Only process non-empty transcripts
                    await self.on_text_callback(transcript)
        except Exception as e:
            print(f"Error handling Deepgram message: {str(e)}")

    async def start_listening(self, meeting_id: str):
        """Start listening for audio from the Zoom meeting"""
        if self.is_listening:
            return

        try:
            print("Starting Deepgram connection...")
            # Create a WebSocket connection to Deepgram
            self.deepgram_socket = await self.deepgram.transcription.live(self.deepgram_params)
            print("Deepgram connection established")

            # Set up the message handler
            async def _handle_messages():
                try:
                    async for msg in self.deepgram_socket:
                        await self._handle_deepgram_message(msg)
                except Exception as e:
                    print(f"Error in message handler: {str(e)}")

            # Start the message handler in the background
            asyncio.create_task(_handle_messages())
            
            self.is_listening = True
            print(f"Now listening for audio in meeting {meeting_id}")
        except Exception as e:
            print(f"Error starting Deepgram connection: {str(e)}")
            raise

    async def stop_listening(self):
        """Stop listening for audio"""
        if self.deepgram_socket:
            try:
                await self.deepgram_socket.close()
            except Exception as e:
                print(f"Error closing Deepgram socket: {str(e)}")
            finally:
                self.deepgram_socket = None
                self.is_listening = False
