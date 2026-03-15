import pyttsx3
import json
import os 
import queue
import webbrowser
from vosk import Model, KaldiRecognizer
import sounddevice as sd

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
def speak(text):
    print("Jarvis: ", text)
    engine.say(text)
    engine.runAndWait()

# Function to check if the Vosk model is available and load it
def load_model():
    path = "vosk-model-small-en-us-0.15"
    if not os.path.exists(path):
        speak("Please download the Vosk model and place it in the project directory.")
        return None
    return path

# Load speech recognition model
model_path = load_model()
if model_path:
    model = Model(model_path)

# speech recognition object 
recognizer = KaldiRecognizer(model, 16000)

# Creating a queue to hold audio data
q = queue.Queue()

# Audio callback function to capture audio data
def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

# main command processing function
def process_command(command):
    print(command)

# main variables
wake_word = "jarvis"
activated = False

# main function
if __name__ == "__main__":
    speak("Initializing Jarvis. Please wait...")

    try:
        # Start the audio stream and listen for wake word
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
            speak("Jarvis is ready.")
            

            while True:
                # Get audio chunk data from the queue
                data = q.get()

                # waiting for the wake word to activate the assistant
                if recognizer.AcceptWaveform(data): 
                    result = json.loads(recognizer.Result()) 
                    text = result.get("text", "")

                    print("You:", text)

                    # wake word detection
                    if not activated and wake_word in text.lower():
                        activated = True
                        speak("Yes, how can I assist you?")

                    data = q.get()
                    if activated and recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        command = result.get("text", "")
                        print("You:", command)

                        if command:
                            process_command(command)
                            activated = False

    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        speak("Shutting down")

    except Exception as e:
        print("Error occurred:", e)
                        
            


   