from typing import Dict
from fastapi import FastAPI, Request, WebSocket
from datetime import datetime
from fastapi.encoders import jsonable_encoder
import uvicorn
from typing import Dict, List
import os
from dotenv import load_dotenv
from groq import Groq
from student_bots import StudentBotManager
from texttospeech import text_to_speech
from audio_processor import AudioProcessor
from fastapi import FastAPI, WebSocket
import json
from pymongo import MongoClient
from typing import Dict
import requests
from fastapi import FastAPI, Request
import uvicorn
from typing import Dict, List
from analytics import SpeechAnalyzer



load_dotenv()

# set up database
MONGO_URL = os.getenv("MONGO_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = MongoClient(MONGO_URL)

database = client.get_database("treehacks-2025")
sessions = database.get_collection("user-sessions")

database2 = client.get_database("sample-mflix")
movies = database2.get_collection("movies")
duration = None


user_id = 1
simulation_id = 1

master_transcript = {
    "text": [],
    "audio_files": None,
}

# Load configuration
with open('data/rtms_credentials.json') as f:
    config = json.load(f)

ZOOM_SECRET_TOKEN = config['Zoom_Webhook_Secret_Token'][0]['token']
VOICEGAIN_API_KEY = os.getenv("VOICEGAIN_API_KEY")

# Using the first set of credentials as default, but you might want to implement credential selection logic
CLIENT_SECRET = config['auth_credentials'][0]['client_secret']

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

master_transcript : List[Dict[str, str]] = []

student_bot_manager = StudentBotManager()
audio_processor = AudioProcessor()

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global master_transcript
    global duration

    await websocket.accept()
    start_time = datetime.now()
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
        # Save the final combined audio to WAV file
        final_audio_path = audio_processor.get_full_audio("final_output.wav")
        if final_audio_path:
            print(f"Final audio saved as {final_audio_path}")
            end_time = datetime.now()
            duration = end_time - start_time
        else:
            print("No audio was recorded")

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

@app.get("/history/{user_id}")
async def get_history(user_id: int):
    """Get the session history from MongoDB."""
    history = list(sessions.find({"user_id": user_id}, {'_id': 0}))
    return {"data": history}

@app.get("/analytics")
async def get_analytics(): 
    global simulation_id
    # URL = "https://api.voicegain.ai" 
    # headers = {
    #     "Authorization": VOICEGAIN_API_KEY,
    # }

    analyzer = SpeechAnalyzer(OPENAI_API_KEY)

    analysis = analyzer.analyze(master_transcript, duration)

    # # start new analytics session

    # # output_buffer = BytesIO()
    # # combined_audio.export(output_buffer, format="wav")
    # # combined_base64_encoding = base64.b64encode(output_buffer.getvalue()).decode("utf-8")
    # combined_base64_encoding = encoding

    # print("SD:LKFJ:SLFJ")

    # sessions.insert_one({
    #         "user_id": user_id,
    #         "transcript": master_transcript,
    #         "simulation_id": simulation_id,
    #         "analytics": {}, 
    #         "audio": encoding,
    #         "config": [],
    #     })

    # simulation_id += 1
    
    # # return 

    # data = {
    #     "audio": {
    #         "source" : {
    #             "inline": combined_base64_encoding
    #         }
    #     },
    #     "asyncMode": "OFF-LINE",
    #     "speakerChannels": [
    #         {
    #         "audioChannelSelector": "mix",
    #         "isAgent": False,
    #         "vadMode": "normal"
    #         }
    #     ]
    # }

    # print("HERE")

    # try:
    #     res =  await requests.post(URL + "/v1/sa", headers=headers, data=data)

    #     print("HERE@")
    #     sessionID = res.json()["saSessionId"]
    #     print(sessionID)

    #     response = await requests.get(URL + f'/sa/{sessionID}/data', headers=headers)

    #     print("MEOWMEOW")

    # except(Exception): 
    #     return {Exception}

    # return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)