import re
import openai
from collections import defaultdict
from openai import OpenAI

FILLER_WORDS = {"um", "uh", "like", "you know", "so", "actually", "basically", "right"}  # Add more if needed

class SpeechAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def extract_teacher_speech(self, transcript, teacher_label="Teacher"):
        """Extract only the teacher's speech from a structured transcript."""
        teacher_text = []
        for entry in transcript:
            if entry["speaker"] == teacher_label:
                teacher_text.append(entry.get("text", "").strip())
        return " ".join(teacher_text)
    
    def detect_emotions(self, text):
        """Detect emotions using OpenAI API. Say in one word"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Analyze the emotion in the following text."},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during emotion detection: {str(e)}")
            return None
    
    def analyze_speech_rate(self, text, duration):
        """Calculate speech rate (words per minute)."""
        if not text or duration <= 0:
            return 0
        words = text.split()
        words_per_minute = len(words) / (duration / 60)
        return round(words_per_minute, 2)
    
    def count_filler_words(self, text):
        """Count occurrences of filler words in the teacher's speech."""
        word_counts = defaultdict(int)
        if text:
            words = re.findall(r'\b\w+\b', text.lower())
            for word in words:
                if word in FILLER_WORDS:
                    word_counts[word] += 1
        return dict(word_counts)
    
    def analyze_teacher_speech(self, transcript, duration):
        """Process the transcript to analyze only the teacher's speech."""
        teacher_text = self.extract_teacher_speech(transcript)
        if not teacher_text:
            return {"error": "No teacher speech detected."}
        
        emotions = self.detect_emotions(teacher_text)
        speech_rate = self.analyze_speech_rate(teacher_text, duration)
        filler_words = self.count_filler_words(teacher_text)
        suggestions = self.generate_suggestions(transcript)
        
        return {
            "emotions": emotions,
            "speech_rate_wpm": speech_rate,
            "filler_words_count": filler_words,
            "suggestions": suggestions
        }
    
    def generate_suggestions(self, transcript):
        """Generate AI-based suggestions using GPT-4."""
        try:
            prompt = """
            Provide a 4-5 sentence improvement summary with constructive feedback.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f'You are an expert in teaching. Provide feedback to the teacher on how to keep student engaged based on: {transcript}'},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating suggestions: {str(e)}")
            return None


client = openai.OpenAI(api_key="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")

analyzer = SpeechAnalyzer(client)


# # """
# # Teacher: Today so we will discuss the solar system.
# # Student: Okay!
# # Teacher: The sun is at the center, and planets orbit around it.
# # Student: Oh, I see lol!
# # """

# result = analyzer.analyze_teacher_speech(transcript, duration=120)
# print(result)
