import subprocess

is_speaking = False

# Function to speak text using Windows built-in speech
def speak(text):

    global is_speaking
    is_speaking = True

    try:

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

    finally:

        is_speaking = False