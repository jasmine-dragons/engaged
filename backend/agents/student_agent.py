from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class StudentAgent:
    def __init__(self, name: str, personality_type: str):
        self.name = name
        self.personality_type = personality_type
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Create the agent's prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are {name}, a student in a classroom with a specific personality type: {personality_type}.
            Respond to the teacher's questions and comments in a way that reflects your personality type.
            Keep responses concise and natural, as if speaking in a real classroom.
            
            Examples for different personality types:
            - enthusiastic: Eager to participate, shows excitement about learning
            - confused: Often needs clarification, asks follow-up questions
            - distracted: May give off-topic responses, needs redirection
            
            Your personality type is: {personality_type}
            
            Remember:
            1. Stay in character as a student
            2. Keep responses brief and natural
            3. React according to your personality type
            4. Use age-appropriate language"""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="chat_history")
        ])
        
        # Create the LLM chain
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            verbose=True
        )
        
        # Initialize chat history
        self.chat_history = []

    async def handle_teacher_input(self, input_text: str) -> str:
        """Handle input from the teacher and generate a response"""
        try:
            # Generate response
            response = await self.chain.arun(
                input=input_text,
                chat_history=self.chat_history
            )
            
            # Update chat history
            self.chat_history.extend([
                ("human", input_text),
                ("assistant", response)
            ])
            
            # Keep chat history manageable
            if len(self.chat_history) > 10:  # Keep last 5 exchanges
                self.chat_history = self.chat_history[-10:]
                
            return response.strip()
        except Exception as e:
            print(f"Error handling teacher input for {self.name}: {str(e)}")
            return f"*{self.name} seems unable to respond right now*"

class StudentAgentManager:
    def __init__(self):
        self.students: Dict[str, StudentAgent] = {}
        
        # Define available personality types
        self.personality_types = [
            "enthusiastic",
            "confused",
            "distracted"
        ]

    def initialize_students(self, number_of_students: int, avatar_types: List[str] = None):
        """Initialize the specified number of student agents"""
        # Clear existing students
        self.students.clear()
        
        # Use provided avatar types or default to cycling through personality types
        if not avatar_types:
            avatar_types = [self.personality_types[i % len(self.personality_types)] 
                          for i in range(number_of_students)]
        
        # Create student agents
        for i in range(number_of_students):
            name = f"Student_{i+1}"
            personality = avatar_types[i % len(avatar_types)]
            self.students[name] = StudentAgent(name, personality)
        
        print(f"Initialized {len(self.students)} student agents")

    async def handle_teacher_input(self, student_name: str, input_text: str) -> str:
        """Handle teacher input for a specific student"""
        if student_name not in self.students:
            return f"Error: Student {student_name} not found"
        
        return await self.students[student_name].handle_teacher_input(input_text)
