import os
from dotenv import load_dotenv
from typing import List, Dict
import asyncio
import random
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

from pymongo import MongoClient

load_dotenv()

# # set up database
# MONGO_URL = os.getenv("MONGO_URL")

# client = MongoClient(MONGO_URL)

# database = client.get_database("treehacks-2025")
# sessions = database.get_collection("user-sessions")

# user_id = 1
# simulation_id = 1139475891
# master_transcript = {"text": "This is a test", 
#                      "speaker": "teacher", 
#                      "timestamp": "12:00:00"
#                      }

# encoding = "test_encoding"

# database2 = client.get_database("sample-mflix")
# movies = database2.get_collection("movies")

# sessions.insert_one({
#         "user_id": user_id,
#         "transcript": master_transcript,
#         "simulation_id": simulation_id,
#         "analytics": {}, 
#         "audio": encoding,
#         "config": [],
#     })

# simulation_id += 1

# Personality templates for different student types
STUDENT_PERSONALITIES = {
    "excitable": {
        "name": "Excitable Student",
        "traits": "Enthusiastic, energetic, eager to participate, sometimes overly excited",
        "behavior": "Frequently raises hand, responds with high energy, shows great excitement about learning",
        "interaction_frequency": 0.8,  # Very high chance of interaction
        "response_style": "Energetic and enthusiastic responses, often speaks quickly and excitedly",
        "cooldown": 2,  # Very quick to respond again
        "voice_id": "TxYttQ18a6GMHv5emxHd"  # Enthusiastic young voice
    },
    "asshole": {
        "name": "Challenging Student",
        "traits": "Competitive, confrontational, opinionated, challenges authority",
        "behavior": "Frequently disagrees, voices strong opinions, can be disruptive",
        "interaction_frequency": 0.7,  # High chance of interaction
        "response_style": "Confrontational responses, often questions or challenges the teacher",
        "cooldown": 4,  # Quick to speak up again
        "voice_id": "A96RjY2GLQ3jVKjkRglb"  # Strong, assertive voice
    },
    "boring": {
        "name": "Reserved Student",
        "traits": "Prefers routine, avoids risks, consistently completes work but lacks creativity",
        "behavior": "Rarely volunteers, gives minimal responses, sticks to basic answers",
        "interaction_frequency": 0.3,  # Low chance of interaction
        "response_style": "Brief, straightforward responses, rarely elaborates",
        "cooldown": 15,  # Long time between interactions
        "voice_id": "9UGJnQaSjBP7pG2dQqjg"  # Monotone voice
    },
    "normal": {
        "name": "Balanced Student",
        "traits": "Well-rounded, friendly, works well with others",
        "behavior": "Participates regularly, gives thoughtful responses, works well in groups",
        "interaction_frequency": 0.5,  # Medium chance of interaction
        "response_style": "Balanced, thoughtful responses with good engagement",
        "cooldown": 8,  # Moderate time between interactions
        "voice_id": "FMBDwjn0TnQbOKpGVlDA"  # Clear, balanced voice
    }
}

class StudentBot:
    def __init__(self, name: str, personality_type: str):
        if personality_type not in STUDENT_PERSONALITIES:
            raise ValueError(f"Invalid personality type: {personality_type}")
        
        self.name = name
        self.personality = STUDENT_PERSONALITIES[personality_type]
        self.chat_model = ChatGroq(
            model="llama-3.3-70b-specdec",
            temperature=0.7
        )
        self.last_interaction_time = datetime.now()
        self.interaction_cooldown = self.personality["cooldown"]

    async def should_interact(self) -> bool:
        """Determine if the student should interact based on personality and cooldown"""
        current_time = datetime.now()
        time_since_last = (current_time - self.last_interaction_time).seconds
        
        # Check cooldown
        if time_since_last < self.interaction_cooldown:
            print(f"{self.name}: On cooldown ({time_since_last}s < {self.interaction_cooldown}s)")
            return False
        
        # Check interaction probability
        roll = random.random()
        should_interact = roll < self.personality["interaction_frequency"]
        print(f"{self.name}: Interaction roll {roll:.2f} vs threshold {self.personality['interaction_frequency']:.2f} -> {should_interact}")
        
        return should_interact

    async def process_teacher_input(self, transcript: Dict[str, str]) -> Dict[str, any]:
        """Process teacher input and generate a response"""
        should_interact = await self.should_interact()
        print(f"\n{self.name}: Deciding to interact -> {should_interact}")
        
        if not should_interact:
            return {
                "student_name": self.name,
                "responded": False,
                "response": None
            }
        
        try:
            self.last_interaction_time = datetime.now()
            print(f"{self.name}: Generating response...")
            
            # Format the context message
            context_message = f"""Context:
Transcript of class so far:\n {str(transcript)}\n

Respond as your student character would in this situation."""
            
            # Generate response using the chat model
            response = await self.chat_model.ainvoke([
                SystemMessage(content=f"""You are {self.name}, a student in a classroom.
Personality: {self.personality['traits']}
Behavior: {self.personality['behavior']}
Response Style: {self.personality['response_style']}

You should respond in a way that reflects your personality. Your responses should be:
1. Brief (1-3 sentences)
2. Natural and conversational
3. Age-appropriate for a student
4. Consistent with your personality traits
5. Sometimes include questions or requests for clarification
6. May include interruptions or tangential thoughts (especially for distracted personality)

Respond with only the verbal response, no additional formatting or explanation."""),
                HumanMessage(content=context_message)
            ])
            
            print(f"{self.name}: Successfully generated response")
            return {
                "student_name": self.name,
                "responded": True,
                "response": response.content
            }
            
        except Exception as e:
            print(f"Error generating response for {self.name}: {str(e)}")
            return {
                "student_name": self.name,
                "responded": False,
                "response": None,
                "error": str(e)
            }

class StudentBotManager:
    def __init__(self):
        self.students: List[StudentBot] = []
        self.current_student: int = 0
    
    def initialize_students(self, student_personalities: List[str]):
        # Create student bots
        self.students = []
        for personality in student_personalities:
            try:
                name = f"student_{personality}"
                student = StudentBot(name, personality)
                self.students.append(student)
                print("[DEBUG]", f"Created student {student.name} with personality {personality}")
            except Exception as e:
                print(f"Error creating student: {str(e)}")
    
    async def process_teacher_input(self, transcript: List[Dict[str, str]]) -> List[Dict[str, any]]:
        if not self.students:
            raise ValueError("No students initialized. Call initialize_students first.")
            
        
        student = self.students[self.current_student]
        self.current_student = (self.current_student + 1) % len(self.students)
        response = await student.process_teacher_input(transcript)

        if response["responded"]:
            return {
                "text": response["response"],
                "speaker": student.name,
                "timestamp": student.last_interaction_time,
                "voice_id": student.personality["voice_id"]
            }

        return None

# Example usage:
async def main():
    # Set random seed for reproducible testing
    random.seed(42)
    
    # Initialize manager and students
    manager = StudentBotManager()
    manager.initialize_students(["excitable", "asshole", "boring", "normal"])
    
    # Example transcripts to test different scenarios
    transcripts = [
        {
            "summary": "The class is learning about photosynthesis. The teacher explained how plants use sunlight to create energy.",
            "local_transcript": "Can anyone tell me what role chlorophyll plays in photosynthesis?"
        },
        {
            "summary": "The class is learning about photosynthesis. A student mentioned chlorophyll helps capture sunlight.",
            "local_transcript": "Excellent point! And what happens to that captured sunlight energy?"
        },
        {
            "summary": "The class is discussing photosynthesis, specifically how chlorophyll captures sunlight and converts it to energy.",
            "local_transcript": "Now, can someone explain why leaves change color in the fall?"
        }
    ]
    
    # Process each transcript
    for i, transcript in enumerate(transcripts, 1):
        print(f"\n=== Testing Transcript {i} ===")
        print(f"Teacher: {transcript['local_transcript']}")
        print("-" * 50)
        
        # Get student responses
        responses = await manager.process_teacher_input([transcript])
        
        # Print responses
        for response in [responses]:
            if response:
                print(f"\n{response['speaker']} says: {response['text']}")
            else:
                print(f"\nNo student responded")
        
        # Wait between transcripts to reset cooldowns
        if i < len(transcripts):
            print("\nWaiting for cooldown reset...")
            await asyncio.sleep(6)

if __name__ == "__main__":
    asyncio.run(main())
