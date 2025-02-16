from dotenv import load_dotenv
import openai
import librosa
import numpy as np
import webrtcvad
import struct
import re
from collections import defaultdict
import wave

load_dotenv()  
# Define filler words
FILLER_WORDS = {"um", "uh", "like", "you know", "so", "actually", "basically", "right"}

class SpeechAnalyzer:
    def __init__(self, openai_api_key):
        """Initialize the speech analyzer with OpenAI API key."""
        self.api_key = openai_api_key  # Store API key as instance variable
        self.client = openai.OpenAI(api_key=openai_api_key)  # Initialize OpenAI client
        self.vad = webrtcvad.Vad(3)  # Initialize VAD with aggressiveness level 3
    
    def transcribe_audio(self, audio_path):
        """Transcribe audio using OpenAI Whisper API."""
        try:
            with open(audio_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return response.text
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            return None

    def detect_emotions(self, text):
        """Detect emotions using OpenAI API."""
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
        """Count occurrences of filler words."""
        word_counts = defaultdict(int)
        if text:
            words = re.findall(r'\b\w+\b', text.lower())
            for word in words:
                if word in FILLER_WORDS:
                    word_counts[word] += 1
        return dict(word_counts)


    def generate_suggestions(self, speech_rate, filler_count):
        """Generate AI-based suggestions using GPT-4."""
        try:
            prompt = f"""
            Provide a 4-5 sentence improvement summary with constructive feedback.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in teaching. Provide feedback to the teacher on how to keep student engaged"},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating suggestions: {str(e)}")
            return None

    def analyze(self, audio_path):
        """Main analysis function."""
        try:
            # Load audio
            import soundfile as sf
            audio, sr = sf.read(audio_path)
            if len(audio.shape) > 1:
                audio = audio.mean(axis=1)  # Convert to mono if stereo
            duration = librosa.get_duration(y=audio, sr=sr)
            
            # Run analysis
            results = {
                "transcription": self.transcribe_audio(audio_path),
                "duration": duration,
                "speech_rate": None,
                "filler_words": None,
                "emotions": None,
                "speech_segments": None,
                "suggestions": None
            }
            
            if results["transcription"]:
                results["speech_rate"] = self.analyze_speech_rate(
                    results["transcription"], duration)
                results["filler_words"] = self.count_filler_words(
                    results["transcription"])
                results["emotions"] = self.detect_emotions(
                    results["transcription"])
                results["suggestions"] = self.generate_suggestions(
                    results["speech_rate"], 
                    results["filler_words"])
            
            return results
            
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    import os
    
    # Make sure to set your OpenAI API key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("Please set your OPENAI_API_KEY environment variable")
    
    analyzer = SpeechAnalyzer(OPENAI_API_KEY)
    # Replace with your audio file path
    results = analyzer.analyze("C:/Users/vadda/vibhahacks/conversation.mp3")
    
    if results:
        print("\nAnalysis Results:")
        print(f"Transcription: {results['transcription']}")
        print(f"Speech Rate: {results['speech_rate']} WPM")
        print(f"Filler Words: {results['filler_words']}")
        print(f"Emotions: {results['emotions']}")
        print(f"\nAI Suggestions:\n{results['suggestions']}")
