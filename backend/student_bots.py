import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
import asyncio
import random
from datetime import datetime
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

load_dotenv()

# Personality templates for different student types
STUDENT_PERSONALITIES = {
    "eager": {
        "name": "Eager Learner",
        "traits": "Enthusiastic, engaged, always ready to participate, asks thoughtful questions",
        "behavior": "Frequently raises hand, responds positively, shows excitement about learning",
        "interaction_frequency": 0.7,  # High chance of interaction
        "response_style": "Energetic and enthusiastic responses, often volunteers information, asks follow-up questions",
        "cooldown": 3  # Quick to respond again
    },
    "shy": {
        "name": "Shy Student",
        "traits": "Quiet, thoughtful, takes time to process, hesitant to speak up",
        "behavior": "Rarely volunteers but gives good answers when called upon",
        "interaction_frequency": 0.3,  # Lower chance of interaction
        "response_style": "Brief, quiet responses, speaks only when confident about the answer",
        "cooldown": 15  # Needs more time between interactions
    },
    "distracted": {
        "name": "Distracted Student",
        "traits": "Easily distracted, sometimes off-topic, but generally well-meaning",
        "behavior": "May ask for repetition, occasionally makes off-topic comments",
        "interaction_frequency": 0.5,  # Medium chance of interaction
        "response_style": "Sometimes off-topic responses, may ask for clarification, occasionally relates to unrelated personal experiences",
        "cooldown": 5  # Moderate cooldown, might get distracted and speak up again soon
    },
    "analytical": {
        "name": "Analytical Thinker",
        "traits": "Detail-oriented, logical, likes to understand the 'why'",
        "behavior": "Asks detailed questions, points out inconsistencies, seeks deeper understanding",
        "interaction_frequency": 0.6,  # Medium-high chance of interaction
        "response_style": "Detailed, logical responses, often asks about underlying principles and mechanisms",
        "cooldown": 8  # Takes time to formulate next thought
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
Summary of class so far: {transcript['summary']}
Teacher just said: {transcript['local_transcript']}

Respond as your student character would in this situation."""
            
            # Generate response using the chat model
            response = await self.chat_model.ainvoke([
                SystemMessage(content=f"""You are {self.name}, a student in a classroom.
Personality: {self.personality['traits']}
Behavior: {self.personality['behavior']}
Response Style: {self.personality['response_style']}

You should respond in a way that reflects your personality. Your responses should be:
1. Brief (1-2 sentences)
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
    
    def initialize_students(self, student_configs: List[Dict[str, str]]):
        """
        Initialize student bots with specified configurations
        
        Args:
            student_configs: List of dictionaries with 'name' and 'personality' keys
            Example: [
                {"name": "Alice", "personality": "eager"},
                {"name": "Bob", "personality": "shy"},
                ...
            ]
        """
        self.students = []
        for config in student_configs:
            try:
                student = StudentBot(config["name"], config["personality"])
                self.students.append(student)
                print(f"Created student {student.name} with personality {config['personality']}")
            except Exception as e:
                print(f"Error creating student with config {config}: {str(e)}")
    
    async def process_teacher_input(self, transcript: Dict[str, str]) -> List[Dict[str, any]]:
        """
        Process teacher input and get responses from all students in parallel
        
        Args:
            transcript: Dictionary with 'summary' and 'local_transcript' keys
            
        Returns:
            List of student responses, including non-responses
        """
        if not self.students:
            raise ValueError("No students initialized. Call initialize_students first.")
            
        # Create tasks for all students
        tasks = [
            student.process_teacher_input(transcript)
            for student in self.students
        ]
        
        # Run all tasks concurrently
        responses = await asyncio.gather(*tasks)
        return responses

# Example usage:
async def main():
    # Set random seed for reproducible testing
    random.seed(42)
    
    # Create student configurations
    student_configs = [
        {"name": "Alice", "personality": "eager"},
        {"name": "Bob", "personality": "shy"},
        {"name": "Charlie", "personality": "distracted"},
        {"name": "Diana", "personality": "analytical"}
    ]
    
    # Initialize manager and students
    manager = StudentBotManager()
    manager.initialize_students(student_configs)
    
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
        responses = await manager.process_teacher_input(transcript)
        
        # Print responses
        for response in responses:
            if response["responded"]:
                print(f"\n{response['student_name']} says: {response['response']}")
            else:
                print(f"\n{response['student_name']} did not respond")
        
        # Wait between transcripts to reset cooldowns
        if i < len(transcripts):
            print("\nWaiting for cooldown reset...")
            await asyncio.sleep(6)

if __name__ == "__main__":
    asyncio.run(main())
