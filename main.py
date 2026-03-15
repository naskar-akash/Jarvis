import subprocess
import json
import os 
import queue
import webbrowser
from vosk import Model, KaldiRecognizer
import sounddevice as sd
from rapidfuzz import fuzz



# Function to speak text using Windows built-in speech
def speak(text):
    print("Jarvis:", text)

    command = f'''
    Add-Type -AssemblyName System.Speech;
    $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $speak.SelectVoice("Microsoft Zira Desktop");
    $speak.Rate = 1;
    $speak.Volume = 100;
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

# using a fuzzy maching function instead of strict matching
def is_match(command, keyword):
    return fuzz.partial_ratio(command, keyword) > 80


# main command processing function
def process_command(command):
    command = command.lower()
    if is_match(command, "youtube"):
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

    elif is_match(command, "google"):
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")

    elif is_match(command, "github"):
        webbrowser.open("https://github.com/naskar-akash?tab=repositories")
        speak("Opening GitHub.")

    elif is_match(command, "chatgpt"):
        webbrowser.open("https://chatgpt.com/")
        speak("Opening ChatGPT.")

    elif is_match(command, "email"):
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
        speak("Opening Gmail.")

    elif is_match(command.split()[0], "play"):
        words = command.split()

        if len(words) > 1:
            song = " ".join(words[1:])
            url = f"https://www.youtube.com/results?search_query={song}"
            webbrowser.open(url)
            speak(f"Playing {song}")
        else:
            speak("Please tell me the song name")
    
    elif "stop" in command.lower() or "exit" in command.lower():
        speak("shutting down..")
        os._exit(0)

    else: 
        speak("I did not understand the command.")


# main variables
wake_words = ["jarvis"]
activated = False

# cleaning text function 
def clean_text(text):
    text = text.lower().strip()
    text = text.replace("  ", " ")
    return text



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

   