
pip install pyttsx3

import pyttsx3

# Initialize the TTS engine

engine = pyttsx3.init()

# Set the properties for the voice

engine.setProperty('rate', 150) # Speed of speech
engine.setProperty('volume', 2) # volume (0.0 t0 1)

# Convert text to speech

text = " Hey I'm Kev, how are you?"

engine.say(text)

# Wait until the speech is complete

engine.runAndWait()
