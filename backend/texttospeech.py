import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save
import io

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("ELEVENLABS_API_KEY")

# Initialize the ElevenLabs client with the API key
client = ElevenLabs(api_key=api_key)

# Generate the audio
audio_stream_avator1 = client.text_to_speech.convert(
    text="The first move is what sets everything in motion.",
    voice_id="TxYttQ18a6GMHv5emxHd",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

# Save the audio to a file
audio_file = "avator1.mp3"
save(audio_stream_avator1, audio_file)

audio_stream_avator2 = client.text_to_speech.convert(
    text="The first move is what sets everything in motion.",
    voice_id="A96RjY2GLQ3jVKjkRglb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

# Save the audio to a file
audio_file = "avator2.mp3"
save(audio_stream_avator2, audio_file)

audio_stream_avator3 = client.text_to_speech.convert(
    text="The first move is what sets everything in motion.",
    voice_id="9UGJnQaSjBP7pG2dQqjg",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

# Save the audio to a file
audio_file = "avator3.mp3"
save(audio_stream_avator3, audio_file)

audio_stream_avator4 = client.text_to_speech.convert(
    text="The first move is what sets everything in motion.",
    voice_id="FMBDwjn0TnQbOKpGVlDA",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

# Save the audio to a file
audio_file = "avator4.mp3"
save(audio_stream_avator4, audio_file)




