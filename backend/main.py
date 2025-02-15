from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from datetime import datetime, timedelta
from zoomus import ZoomClient
from dotenv import load_dotenv
import uvicorn
from agents.student_agent import StudentAgentManager
from agents.zoom_bot_manager import ZoomBotManager
from agents.speech_to_text import SpeechToTextManager
import asyncio

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="AI Student Practice Platform")

# Initialize managers
zoom_client = ZoomClient(
    api_account_id=os.getenv("ZOOM_ACCOUNT_ID"),
    client_id=os.getenv("ZOOM_CLIENT_ID"),
    client_secret=os.getenv("ZOOM_CLIENT_SECRET")
)

zoom_bot_manager = ZoomBotManager(
    api_key=os.getenv("ZOOM_API_KEY"),
    api_secret=os.getenv("ZOOM_API_SECRET"),
    account_id=os.getenv("ZOOM_ACCOUNT_ID")
)

student_manager = StudentAgentManager()

class PracticeSessionConfig(BaseModel):
    number_of_students: int
    student_avatar_types: list[str]
    session_duration_minutes: int = 60

class MeetingResponse(BaseModel):
    join_url: str
    meeting_id: str
    password: str
    host_key: str
    config: PracticeSessionConfig

async def handle_teacher_speech(text: str, meeting_id: str):
    """Handle converted speech from teacher"""
    try:
        # Get responses from all student agents
        responses = await student_manager.broadcast_message(text)
        
        # Send each response to the Zoom chat
        for response in responses:
            student_name = response["student_name"]
            message = response["response"]
            await zoom_bot_manager.send_chat_message(
                meeting_id=meeting_id,
                student_name=student_name,
                message=message
            )
    except Exception as e:
        print(f"Error handling teacher speech: {str(e)}")

@app.post("/create-practice-session", response_model=MeetingResponse)
async def create_practice_session(config: PracticeSessionConfig):
    try:
        # Initialize student agents
        student_manager.initialize_students(
            number_of_students=config.number_of_students,
            avatar_types=config.student_avatar_types
        )

        # Get user information (first user in the account)
        user_list_response = zoom_client.user.list()
        user_list = user_list_response.json()
        if not user_list.get('users'):
            raise HTTPException(status_code=500, detail="No users found in Zoom account")
        
        user_id = user_list['users'][0]['id']
        
        # Create a Zoom meeting
        meeting_response = zoom_client.meeting.create(
            user_id=user_id,
            topic=f"AI Student Practice Session ({config.number_of_students} students)",
            type=2,  # Scheduled meeting
            start_time=datetime.utcnow() + timedelta(minutes=1),
            duration=config.session_duration_minutes,
            settings={
                "host_video": True,
                "participant_video": True,
                "join_before_host": True,
                "mute_upon_entry": False,
                "waiting_room": False,
                "meeting_authentication": False
            }
        )
        
        meeting_details = meeting_response.json()
        meeting_id = meeting_details.get("id")
        
        if not meeting_id:
            raise HTTPException(status_code=500, detail="Failed to create Zoom meeting")

        # Create bot participants for each student
        student_names = [f"Student_{i+1}" for i in range(config.number_of_students)]

        print(student_names)

        await zoom_bot_manager.create_bot_participants(str(meeting_id), student_names)
        print("GOT HERE")

        # Initialize speech-to-text manager
        stt_manager = SpeechToTextManager(
            on_text_callback=lambda text: handle_teacher_speech(text, str(meeting_id))
        )
        await stt_manager.start_listening(str(meeting_id))

        # Join meeting with all bot participants
        for student_name in student_names:
            await zoom_bot_manager.join_meeting(str(meeting_id), student_name)

        return MeetingResponse(
            join_url=meeting_details.get("join_url"),
            meeting_id=str(meeting_id),
            password=meeting_details.get("password", ""),
            host_key=meeting_details.get("h323_password", ""),
            config=config
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
