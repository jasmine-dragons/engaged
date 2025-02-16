import json
import hmac
import hashlib
from collections import defaultdict
from typing import Optional, Dict, Any, Union
import websockets
import asyncio
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn
import base64
from io import BytesIO
import numpy as np
from typing import Dict, List, Optional, Union, Deque
from collections import deque
import time
from dataclasses import dataclass
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv
import soundfile as sf
from groq import Groq
import uuid
import wave
import struct

load_dotenv()

# Load configuration
with open('data/rtms_credentials.json') as f:
    config = json.load(f)

ZOOM_SECRET_TOKEN = config['Zoom_Webhook_Secret_Token'][0]['token']
# Using the first set of credentials as default, but you might want to implement credential selection logic
CLIENT_SECRET = config['auth_credentials'][0]['client_secret']

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Track active connections
active_connections = defaultdict(dict)

app = FastAPI()

class URLValidationResponse(BaseModel):
    plainToken: str
    encryptedToken: str

class StandardResponse(BaseModel):
    status: str

class RTMSPayload(BaseModel):
    event: Optional[str]
    payload: Optional[Dict[str, Any]]

def generate_signature(client_id: str, meeting_uuid: str, stream_id: str, secret: str) -> str:
    """Generate HMAC signature for RTMS authentication."""
    message = f"{client_id},{meeting_uuid},{stream_id}"
    return hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

@dataclass
class AudioChunk:
    data: str  # base64 encoded Int16 PCM data
    timestamp: int
    user_id: int

class AudioProcessor:
    def __init__(self, buffer_duration: float = 3.0, sample_rate: int = 16000):
        """
        Initialize audio processor
        buffer_duration: How many seconds of audio to buffer before processing
        sample_rate: Sample rate of the audio in Hz (default 16kHz)
        """
        self.buffer: Dict[int, Deque[AudioChunk]] = defaultdict(lambda: deque())
        self.buffer_duration = buffer_duration
        self.sample_rate = sample_rate
        self.chunk_size = 320  # 20ms at 16kHz = 320 samples
        self.executor = ThreadPoolExecutor(max_workers=2)
        print(f"Initialized AudioProcessor with {sample_rate}Hz sample rate, "
              f"chunk size: {self.chunk_size} samples, "
              f"buffer duration: {buffer_duration}s")

    def add_chunk(self, chunk: AudioChunk) -> Optional[List[AudioChunk]]:
        """Add a new audio chunk to the buffer."""
        user_buffer = self.buffer[chunk.user_id]
        user_buffer.append(chunk)
        
        if self._is_buffer_ready(user_buffer):
            chunks_to_process = list(user_buffer)
            user_buffer.clear()
            return chunks_to_process
        return None
    
    def _is_buffer_ready(self, buffer: Deque[AudioChunk]) -> bool:
        """Check if we have enough chunks for processing"""
        if not buffer:
            return False
        expected_chunks = int((self.buffer_duration * 1000) / 20)  # 20ms per chunk
        return len(buffer) >= expected_chunks

    def _create_wav_file(self, audio_data: bytes, filename: str) -> None:
        """
        Create a WAV file from Int16 PCM data
        audio_data: Raw bytes containing Int16 PCM samples
        """
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 16-bit audio
            wav_file.setframerate(self.sample_rate)
            
            # Verify we have the correct number of bytes
            num_samples = len(audio_data) // 2  # 2 bytes per sample
            expected_samples = len(self.buffer) * self.chunk_size
            print(f"Number of samples: {num_samples}, Expected: {expected_samples}")
            
            wav_file.writeframes(audio_data)

    async def process_chunks(self, chunks: List[AudioChunk]) -> str:
        """Process audio chunks and return transcribed text"""
        try:
            print(f"Processing {len(chunks)} chunks")
            total_duration = len(chunks) * 0.02  # 20ms per chunk
            print(f"Total audio duration: {total_duration:.2f} seconds")
            expected_samples = len(chunks) * self.chunk_size
            
            # Decode and combine all base64 audio data
            raw_audio = bytearray()
            for chunk in chunks:
                # Decode base64 to bytes (should be Int16 PCM data)
                chunk_data = base64.b64decode(chunk.data)
                # Verify chunk size
                chunk_samples = len(chunk_data) // 2  # 2 bytes per sample
                print(f"Chunk samples: {chunk_samples}, Expected: {self.chunk_size}")
                raw_audio.extend(chunk_data)
            
            print(f"Combined raw audio size: {len(raw_audio)} bytes")
            print(f"Total samples: {len(raw_audio) // 2}")
            
            # Verify we have complete 16-bit samples
            if len(raw_audio) % 2 != 0:
                print("Warning: Incomplete sample at end of buffer")
                raw_audio = raw_audio[:-1]
            
            # Create a unique filename for this audio
            filename = f"audio_{uuid.uuid4()}.wav"
            
            try:
                # Create WAV file with proper headers
                self._create_wav_file(bytes(raw_audio), filename)
                
                # Open the audio file for Groq
                with open(filename, "rb") as file:
                    transcription = groq_client.audio.transcriptions.create(
                        file=(filename, file.read()),
                        model="distil-whisper-large-v3-en",
                        response_format="json",
                        language="en",
                        temperature=0.0
                    )
                
                # Clean up the temporary file
                os.remove(filename)
                
                return transcription.text
                
            except Exception as e:
                if os.path.exists(filename):
                    os.remove(filename)
                raise e
            
        except Exception as e:
            print(f"Error processing audio chunks: {e}")
            return f"Error: {str(e)}"

async def connect_to_media_websocket(
    endpoint: str,
    client_id: str,
    meeting_uuid: str,
    stream_id: str,
    media_type: str
) -> None:
    """Connect to the RTMS media WebSocket server."""
    connection_id = f"{meeting_uuid}_{stream_id}_{media_type}"

    # Close existing media connection if any
    if connection_id in active_connections:
        await active_connections[connection_id]['ws'].close()
        del active_connections[connection_id]

    if media_type != 'audio':
        return  # Only process audio
    
    # Initialize audio processor if needed
    audio_processor = AudioProcessor() if media_type == 'audio' else None
    
    try:
        async with websockets.connect(endpoint, ssl=None) as ws:
            active_connections[connection_id] = {'ws': ws}
            
            media_signature = generate_signature(client_id, meeting_uuid, stream_id, CLIENT_SECRET)
            handshake_message = {
                "msg_type": "DATA_HAND_SHAKE_REQ",
                "protocol_version": 1,
                "meeting_uuid": meeting_uuid,
                "rtms_stream_id": stream_id,
                "signature": media_signature,
                "payload_encryption": False
            }
            await ws.send(json.dumps(handshake_message))

            async for message in ws:
                data = json.loads(message)
                
                if media_type == 'audio' and data['msg_type'] == 'MEDIA_DATA_AUDIO':
                    content = data['content']
                    chunk = AudioChunk(
                        data=content['data'],
                        timestamp=content['timestamp'],
                        user_id=content['user_id']
                    )
                    
                    if chunks_to_process := audio_processor.add_chunk(chunk):
                        # Process audio chunks in background
                        transcription = await audio_processor.process_chunks(chunks_to_process)
                        print(f"Transcription for user {chunk.user_id}: {transcription}")

    except Exception as e:
        print(f"{media_type} WebSocket error: {e}")
    finally:
        if connection_id in active_connections:
            del active_connections[connection_id]

async def connect_to_rtms_websocket(
    client_id: str,
    meeting_uuid: str,
    stream_id: str,
    server_url: str
) -> None:
    """Connect to the RTMS signaling WebSocket server."""
    connection_id = f"{meeting_uuid}_{stream_id}"
    
    # Close existing connection if any
    if connection_id in active_connections:
        await active_connections[connection_id]['ws'].close()
        del active_connections[connection_id]

    try:
        async with websockets.connect(server_url, ssl=None) as ws:
            active_connections[connection_id] = {'ws': ws}
            
            signature = generate_signature(client_id, meeting_uuid, stream_id, CLIENT_SECRET)
            handshake_message = {
                "msg_type": "SIGNALING_HAND_SHAKE_REQ",
                "protocol_version": 1,
                "meeting_uuid": meeting_uuid,
                "rtms_stream_id": stream_id,
                "signature": signature
            }
            await ws.send(json.dumps(handshake_message))

            async for message in ws:
                data = json.loads(message)
                
                if data['msg_type'] == "SIGNALING_HAND_SHAKE_RESP":
                    if data['status_code'] == "STATUS_OK":
                        media_urls = data['media_server']['server_urls']
                        
                        # Connect to all available media endpoints
                        for media_type, url in media_urls.items():
                            asyncio.create_task(
                                connect_to_media_websocket(
                                    url,
                                    client_id,
                                    meeting_uuid,
                                    stream_id,
                                    media_type
                                )
                            )
                
                elif data['msg_type'] == "STREAM_STATE_UPDATE":
                    if data['state'] == "TERMINATED":
                        await ws.close()
                        if connection_id in active_connections:
                            del active_connections[connection_id]
                        break
                
                elif data['msg_type'] == "KEEP_ALIVE_REQ":
                    response = {
                        "msg_type": "KEEP_ALIVE_RESP",
                        "timestamp": int(asyncio.get_event_loop().time() * 1000)
                    }
                    await ws.send(json.dumps(response))

    except Exception as e:
        print(f"RTMS WebSocket error: {e}")
    finally:
        if connection_id in active_connections:
            del active_connections[connection_id]

@app.post("/", response_model=Union[URLValidationResponse, StandardResponse])
async def webhook_handler(request: Request):
    """Handle incoming Zoom webhooks."""
    data = await request.json()
    event = data.get('event')
    payload = data.get('payload', {})

    # Handle Zoom Webhook validation
    if event == 'endpoint.url_validation' and payload.get('plainToken'):
        print('Received URL validation request:', {
            'event': event,
            'plainToken': payload['plainToken']
        })

        hash_for_validate = hmac.new(
            ZOOM_SECRET_TOKEN.encode(),
            payload['plainToken'].encode(),
            hashlib.sha256
        ).hexdigest()

        response = URLValidationResponse(
            plainToken=payload['plainToken'],
            encryptedToken=hash_for_validate
        )
        
        print('Sending URL validation response:', response.dict())
        return response

    # Handle RTMS start event
    if (payload.get('event') == 'meeting.rtms.started' and 
        payload.get('payload', {}).get('object')):
        
        client_id = data.get('clientId')
        meeting_data = payload['payload']['object']
        meeting_uuid = meeting_data.get('meeting_uuid')
        rtms_stream_id = meeting_data.get('rtms_stream_id')
        server_urls = meeting_data.get('server_urls')

        if all([client_id, meeting_uuid, rtms_stream_id, server_urls]):
            asyncio.create_task(
                connect_to_rtms_websocket(
                    client_id,
                    meeting_uuid,
                    rtms_stream_id,
                    server_urls
                )
            )

    return StandardResponse(status="ok")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up connections on shutdown."""
    for connections in active_connections.values():
        if 'ws' in connections:
            await connections['ws'].close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)