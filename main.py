import subprocess
import json
import os 
import queue
import webbrowser
from vosk import Model, KaldiRecognizer
import sounddevice as sd


# Function to speak text using Windows built-in speech
def speak(text):
    print("Jarvis:", text)

    command = f'''
    Add-Type -AssemblyName System.Speech;
    $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $speak.Speak("{text}");
    '''

    subprocess.run(["powershell", "-Command", command])


# Function to check if the Vosk model is available and load it
def load_model():
    path = "vosk-model-small-en-us-0.15"
    if not os.path.exists(path):
        speak("Please download the Vosk model.")
        return None
    return Model(path)

model = load_model()
if model is None:
    exit()
# speech recognition object 
recognizer = KaldiRecognizer(model, 16000)

# Creating a queue to hold audio data
q = queue.Queue()


# Audio callback function to capture audio data
def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))


# main command processing function
def process_command(command):
    if "youtube" in command.lower():
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

    elif "google" in command.lower():
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    
    elif "stop" in command.lower() or "exit" in command.lower():
        speak("shutting down..")
        os._exit(0)

    else: 
        speak("I did not understand the command.")


# main variables
wake_word = "jarvis"
activated = False



# main function
if __name__ == "__main__":
    speak("Initializing Jarvis.")

    try:
        # Start the audio stream and listen for wake word
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
            print("Listening...")

            while True:
                # Get audio chunk data from the queue
                data = q.get()

                # waiting for the wake word to activate the assistant
                if recognizer.AcceptWaveform(data): 
                    result = json.loads(recognizer.Result()) 
                    text = result.get("text", "")

                    print("Recognized command:", text)

                    # wake word detection
                    if not activated and wake_word in text.lower():
                        activated = True
                        speak("Yes, how can I assist you?")

                    # Command listening
                    elif activated:
                        if text:
                            process_command(text)

                        recognizer.Reset()

    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        speak("Shutting down")

    except Exception as e:
        print("Error occurred:", e)