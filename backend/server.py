import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from dotenv import load_dotenv
from audio_processor import AudioProcessor
from student_bots import StudentBotManager
from texttospeech import text_to_speech
from analytics import SpeechAnalyzer
from typing import Dict, List
import base64

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationSession:
    def __init__(self):
        self.audio_processor = AudioProcessor()
        self.student_bot_manager = StudentBotManager()
        self.start_time = None
        self.transcript: List[Dict] = []
        
    async def handle_event(self, websocket: WebSocket, event: str, payload: dict) -> None:
        if event == "START-SIM":
            await self.handle_start_sim(websocket, payload)
        elif event == "AUDIO-CHUNK":
            await self.handle_audio_chunk(websocket, payload)
        elif event == "END-SIM":
            await self.handle_end_sim(websocket)
            
    async def handle_start_sim(self, websocket: WebSocket, payload: dict) -> None:
        """Handle simulation start event"""
        student_personalities = payload.get("studentPersonalities", [])
        if not student_personalities:
            await websocket.send_json({
                "event": "ERROR",
                "payload": {"message": "No student personalities provided"}
            })
            return
            
        self.student_bot_manager.initialize_students(student_personalities)
        self.start_time = datetime.now()
        
        await websocket.send_json({
            "event": "SIM-STARTED",
            "payload": {"message": "Simulation started successfully"}
        })
        
    async def handle_audio_chunk(self, websocket: WebSocket, payload: dict) -> None:
        """Handle incoming audio chunk"""
        try:
            # Decode base64 audio data
            audio_bytes = base64.b64decode(payload["audio"])
            
            # Process and transcribe audio
            self.audio_processor.process_chunk(audio_bytes)
            transcription = await self.audio_processor.transcribe_latest()
            
            if transcription:
                # Add to transcript
                self.transcript.append({
                    "text": transcription,
                    "speaker": "teacher",
                    "timestamp": datetime.now().isoformat()
                })
                
                # Get student response
                response = await self.student_bot_manager.process_teacher_input(self.transcript)
                
                if response:
                    # Add student response to transcript
                    self.transcript.append({
                        "text": response["text"],
                        "speaker": response["speaker"],
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Generate audio response
                    audio_stream = text_to_speech(response["text"], response["voice_id"])
                    if audio_stream:
                        # Convert audio to base64
                        audio_base64 = base64.b64encode(audio_stream).decode('utf-8')
                        
                        # Send audio response
                        await websocket.send_json({
                            "event": "STUDENT-AUDIO",
                            "payload": {
                                "audio": audio_base64,
                                "text": response["text"],
                                "speaker": response["speaker"]
                            }
                        })
                        
        except Exception as e:
            await websocket.send_json({
                "event": "ERROR",
                "payload": {"message": f"Error processing audio: {str(e)}"}
            })
            
    async def handle_end_sim(self, websocket: WebSocket) -> None:
        """Handle simulation end event"""
        try:
            end_time = datetime.now()
            duration = end_time - self.start_time if self.start_time else None
            
            # Generate analytics
            analyzer = SpeechAnalyzer(os.getenv("OPENAI_API_KEY"))
            analysis = analyzer.analyze(self.transcript, duration)
            
            # Send final analytics
            await websocket.send_json({
                "event": "SIM-ENDED",
                "payload": {
                    "transcript": self.transcript,
                    "analytics": analysis,
                    "duration": str(duration) if duration else None
                }
            })
            
        except Exception as e:
            await websocket.send_json({
                "event": "ERROR",
                "payload": {"message": f"Error ending simulation: {str(e)}"}
            })
            
        finally:
            await websocket.close()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session = SimulationSession()
    
    try:
        while True:
            # Receive JSON message
            message = await websocket.receive_json()
            event = message.get("event")
            payload = message.get("payload", {})
            
            if not event:
                await websocket.send_json({
                    "event": "ERROR",
                    "payload": {"message": "No event specified"}
                })
                continue
                
            await session.handle_event(websocket, event, payload)
            
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "event": "ERROR",
                "payload": {"message": f"WebSocket error: {str(e)}"}
            })
        except:
            pass
    finally:
        try:
            await websocket.close()
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)