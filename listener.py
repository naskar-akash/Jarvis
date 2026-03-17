from vosk import Model
import os 
import queue
import sounddevice as sd
from speech import speak

# Queue to store incoming audio chunks from microphone
q = queue.Queue()

# Audio callback function to capture audio data
def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

# Function to check if the Vosk model is available and load it
def load_model():
    path = "vosk-model-small-en-us-0.15"
    if not os.path.exists(path):
        speak("Please download the Vosk model.")
        return None
    return Model(path)

def start_stream(recognizer):
     # Start the audio stream and listen for wake word
     return sd.RawInputStream(
        samplerate=16000,
        blocksize=4000,
        dtype='int16',
        channels=1,
        callback=audio_callback
    ) 