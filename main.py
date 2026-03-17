import speech as sp
import json
import os 
from vosk import KaldiRecognizer
import sounddevice as sd
from utils import clean_text
from command import process_command
from dotenv import load_dotenv
import time
from listener import q, load_model, start_stream


load_dotenv() # Loading environment variables

# main variables
wake_word = os.getenv("WAKE_WORD")
activated = False


# main function
if __name__ == "__main__":
    sp.speak("Initializing Jarvis.")

    try:
        # load vosk model
        model = load_model()
        if model is None:
            sp.speak("Model not found!")
            exit()

        recognizer = KaldiRecognizer(model, 16000)
        with start_stream(recognizer):
            print("Listening...")

            while True:

                if sp.is_speaking:
                    continue

                # Get audio chunk data from the queue
                data = q.get()

                # waiting for the wake word to activate the assistant
                if recognizer.AcceptWaveform(data): 
                    result = json.loads(recognizer.Result()) 
                    text = clean_text(result.get("text", ""))

                    print("You:", text)

                    # wake word detection
                    if not activated and wake_word in text.lower():
                        activated = True
                        sp.speak("Yes, what can I do?")
                        time.sleep(0.5)

                    # Command listening
                    elif activated:
                        if text:
                            process_command(text)

                        activated = False
                        recognizer.Reset()

    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        sp.speak("Shutting down")

    except Exception as e:
        print("Error occurred:", e)

   