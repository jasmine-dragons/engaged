import asyncio
from doctest import master
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

mongo_client = MongoClient(MONGO_URL)

database = mongo_client.get_database("treehacks-2025")
sessions = database.get_collection("user-sessions")

user_id = 2
simulation_id = 1

VOICEGAIN_API_KEY = os.getenv("VOICEGAIN_API_KEY")

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

master_transcript : List[Dict[str, str]] = []

student_bot_manager = StudentBotManager()
audio_processor = AudioProcessor()

app = FastAPI()

async def handle_audio_chunk(websocket: WebSocket, audio_chunk: bytes):
    global running
    if not running:
        return
    audio_processor.process_chunk(audio_chunk)
    transcription = await audio_processor.transcribe_latest()

    print("Transcription: ", transcription)

    master_transcript.append({
        "text": transcription,
        "speaker": "teacher",
        "timestamp": datetime.now()
    })

    if not running:
        return
    response = await student_bot_manager.process_teacher_input(master_transcript)
    if response:
        master_transcript.append({
            "text": response["text"],
            "speaker": response["speaker"],
            "timestamp": response["timestamp"],
        })
        audio_stream = text_to_speech(response["text"], response["voice_id"])
        if not running:
            return
        await websocket.send_json({"type": "about-to-speak", "studentName": response["speaker"]})
        await websocket.send_bytes(audio_stream)

tasks: list[asyncio.Task] = []
running = False

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global master_transcript
    global duration
    global tasks, running

    await websocket.accept()
    start_time = datetime.now()
    tasks = []
    running = True
    await websocket.send_json({"type": "students", "students": [[x.name, x.type, x.personality] for x in student_bot_manager.students]})
    try:
        while True:
            print(master_transcript)
            audio_chunk = await websocket.receive_bytes()
            tasks.append(asyncio.create_task(handle_audio_chunk(websocket, audio_chunk)))
            
    except Exception as e:
        print(f"WebSocket error: {e}")

    finally:
        running = False
        # Save the final combined audio to WebM file
        final_audio_path = audio_processor.get_full_audio("final_output.webm")
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
    global master_transcript
    master_transcript = []

    data = await request.json()

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
    return {"data": [{**d, "simulation_id_str": str(d["simulation_id"])} for d in history]}

@app.get("/sim/{simulation_id}")
async def get_sim(simulation_id: int):
    """Get the simulation by ID from MongoDB."""
    simulation = list(sessions.find({"simulation_id": simulation_id}, {"_id": 0}))
    return {"data": simulation[0] if len(simulation) > 0 else False}

@app.post("/analytics")
async def get_analytics(): 
    import random

    global simulation_id
    global tasks


    await asyncio.gather(*tasks)
    tasks = []
    
    analyzer = SpeechAnalyzer(OPENAI_API_KEY)

#     duration= 1000
#     master_transcript = [
#     {"text": "Today so we will discuss the solar system.", 
#      "speaker": "Teacher", 
#      "timestamp": "00:00:00"},
#     {"text": "Okay!", 
#      "speaker": "Student", 
#      "timestamp": "00:00:10"},
#     {"text": "The sun is at the center, and planets orbit around it.", 
#      "speaker": "Teacher", 
#      "timestamp": "00:00:20"},
#     {"text": "Oh, I see lol!", 
#      "speaker": "Student", 
#      "timestamp": "00:00:30"}
# ]


    analysis = analyzer.analyze_teacher_speech(master_transcript, duration)

    configs = [x.personality for x in student_bot_manager.students]

    simulation_id = random.randint(0, (2**63) - 1)

    sim_id = simulation_id
    new_object = {
            "user_id": user_id,
            "transcript": master_transcript,
            "simulation_id": simulation_id,
            "analytics": analysis, 
            # "audio": encoding,
            "config": configs,
            "personalities": [x.type for x in student_bot_manager.students],
            "timestamp": datetime.now(),
        }
    print('INSERT', new_object)
    sessions.insert_one(new_object)

    simulation_id += 1

    return {"simId": str(sim_id), "analysis": analysis}

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