from typing import Dict
from fastapi import FastAPI, Request, HTTPException, WebSocket
from datetime import datetime
import uvicorn
from typing import Dict, List
import os
from dotenv import load_dotenv
from groq import Groq
from student_bots import StudentBotManager
from texttospeech import text_to_speech
from audio_processor import AudioProcessor
from fastapi import FastAPI, WebSocket

load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

master_transcript : List[Dict[str, str]] = []

student_bot_manager = StudentBotManager()
audio_processor = AudioProcessor()

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global master_transcript

    await websocket.accept()
    try:
        while True:
            audio_chunk = await websocket.receive_bytes()
            audio_processor.process_chunk(audio_chunk)
            transcription = await audio_processor.transcribe_latest()

            master_transcript.append({
                "text": transcription,
                "speaker": "teacher",
                "timestamp": datetime.now()
            })

            response = student_bot_manager.process_teacher_input(master_transcript)
            if(response):
                master_transcript.append({
                    "text": response["response"],
                    "speaker": response["speaker"],
                    "timestamp": datetime.now(),
                })
                audio_stream = text_to_speech(response["text"], response["voice_id"])
                await websocket.send_bytes(audio_stream)
    except Exception as e:
        print(f"WebSocket error: {e}")

    finally:
        # Merge all audio segments into one final WAV file
        final_audio = sum(AudioProcessor.buffer)  # Concatenate segments
        final_audio.export("final_output.wav", format="wav")
        print("Final audio saved as final_output.wav")

        await websocket.close()



@app.post("/start-sim")
async def start_sim(request: Request):
    """Start the simulation."""
    data = request.json()

    student_personalities = data.get("studentPersonalities")
    if not student_personalities:
        return {"message": "No student personalities provided"}

    # Start the simulation
    try:
        student_bot_manager.initialize_students(student_personalities)        

    except Exception as e:
        return {"message": f"Error starting simulation: {e}"}

    return {"message": "Simulation started"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)