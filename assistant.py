from gtts import gTTS
import os
import tempfile
import pygame
import threading
from voice import speak
import google.generativeai as genai

import re
import hashlib
import subprocess
import multiprocessing
from gemini_api import get_gemini_response 

AUDIO_CACHE = {}

def clean_text(text):
    """Removes unwanted characters like '*' and trims spaces."""
    text = re.sub(r'[*_]', '', text) 
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def generate_audio_filename(text):
    """Creates a unique filename for caching."""
    hash_id = hashlib.md5(text.encode()).hexdigest()
    return f"{hash_id}.mp3"

def play_audio(file_path):
    """Plays audio quickly using system defaults."""
    if os.name == "nt":  # Windows
        subprocess.run(["start", "", file_path], shell=True)
    else:  # Linux/Mac
        subprocess.run(["mpg321", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def speak(text):
    """Speaks the text with fast speed."""
    text = clean_text(text)
    
    # Check cache
    filename = generate_audio_filename(text)
    cache_path = os.path.join(tempfile.gettempdir(), filename)

    if filename not in AUDIO_CACHE or not os.path.exists(cache_path):
        tts = gTTS(text=text, lang="en", slow=False)  # Faster speech
        tts.save(cache_path)
        AUDIO_CACHE[filename] = cache_path

    # Play in a separate process
    process = multiprocessing.Process(target=play_audio, args=(cache_path,))
    process.start()

def process_input(text):
    """Processes user input, fetches AI response, and speaks it."""
    text = clean_text(text)
    response = get_gemini_response(text)
    speak(response)
    return response 
 

pygame.mixer.init()

def speak(text):
    """Convert text to speech and play it."""
    if not text:
        return

    temp_file = os.path.join(tempfile.gettempdir(), "assistant_response.mp3")

    # Generate speech
    tts = gTTS(text=text, lang="en")
    tts.save(temp_file)

    # Play audio in a separate thread
    def play_audio():
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    threading.Thread(target=play_audio).start()

from gemini_api import get_gemini_response

def get_gemini_response(prompt):
    """Generate AI response using Gemini API."""
    model = genai.GenerativeModel("gemini-2.0-flash")  
    response = model.generate_content(prompt)
    return response.text

def process_input(text, label=None):
    """Processes user input and updates the GUI label if provided."""
    print(f"Processing: {text}")

    # Get AI-generated response
    response = get_gemini_response(text)

    print(f"AI Response: {response}")
    if label:
        label.text = response 

    speak(response) 
    return response

