from speech import speak
import json
import os 
import queue
from vosk import Model, KaldiRecognizer
import sounddevice as sd
from utils import clean_text
from command import process_command



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



# main variables
wake_words = ["jarvis"]
activated = False



# main function
if __name__ == "__main__":
    speak("Initializing Jarvis.")

    try:
        # Start the audio stream and listen for wake word
        with sd.RawInputStream(samplerate=16000, blocksize=4000, dtype='int16', channels=1, callback=audio_callback):
            print("Listening...")

            while True:
                # Get audio chunk data from the queue
                data = q.get()

                # waiting for the wake word to activate the assistant
                if recognizer.AcceptWaveform(data): 
                    result = json.loads(recognizer.Result()) 
                    text = clean_text(result.get("text", ""))

                    print("You:", text)

                    # wake word detection
                    if not activated and any(word in text.lower() for word in wake_words):
                        activated = True
                        speak("Yes, what can I do?")

                    # Command listening
                    elif activated:
                        if text:
                            process_command(text)

                        activated = False
                        recognizer.Reset()

    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        speak("Shutting down")

    except Exception as e:
        print("Error occurred:", e)

   