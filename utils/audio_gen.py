import os
import time
from gtts import gTTS

def generate_audio(text):
    """
    Converts text to an MP3 file using gTTS.
    """
    if not text:
        return None
    
    # Generate unique filename
    filename = f"summary_{int(time.time())}.mp3"
    filepath = os.path.join("static/audio", filename)
    
    try:
        # Create audio object
        tts = gTTS(text=text, lang='en')
        # Save audio file
        tts.save(filepath)
        return filename
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
