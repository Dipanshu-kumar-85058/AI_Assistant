import sounddevice as sd
import numpy as np
import wavio
import speech_recognition as sr
import gtts
import os
import re

# Audio recording settings
SAMPLE_RATE = 44100
DURATION = 5  # Seconds

def record_audio(filename="audio.wav"):
    """Records audio for a set duration and saves it as a WAV file."""
    print("Listening...")
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
    sd.wait()
    wavio.write(filename, audio_data, SAMPLE_RATE, sampwidth=2)
    print("Recording complete.")

def recognize_audio(filename="audio.wav"):
    """Converts recorded speech to text using Google Speech Recognition."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        text = re.sub(r"[*]", "", text) 
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError:
        return "API is not responding. Check your internet connection."

def listen_for_command():
    """Records audio and converts it to text."""
    record_audio()
    return recognize_audio()

def speak(text):
    """Converts text to speech and plays the audio."""
    try:
        text = re.sub(r"[*]", "", text)
        tts = gtts.gTTS(text, lang="en", slow=False)
        tts.save("response.mp3")

        # Play the audio
        if os.name == "nt":  # Windows
            os.system("start response.mp3")
        else:  # macOS/Linux
            os.system("mpg321 response.mp3 &")

        print(f"AI: {text}")
    except Exception as e:
        print(f"Speech Error: {e}")

