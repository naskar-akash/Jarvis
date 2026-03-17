import webbrowser
import os
from utils import is_match
from speech import speak


# function to open the website through key word
def open_website(url, name):
    webbrowser.open(url)
    speak(f"Openning {name}")

# function to play music
def play_music(command):
    song = command.replace("play", "").strip()
    if song:
        url = f"https://www.youtube.com/results?search_query={song}"
        webbrowser.open(url)
        speak(f"Playing {song}")
    else:
        speak("Please tell me the song name")

# main function to process the commands
def process_command(command):
    command = command.lower()

    actions = [
        ("youtube", lambda: open_website("https://www.youtube.com", "Youtube")),
        ("google", lambda: open_website("https://www.google.com", "Google")),
        ("github", lambda: open_website("https://github.com/naskar-akash?tab=repositories", "GitHub")),
        ("chatgpt", lambda: open_website("https://chatgpt.com/", "ChatGPT")),
        ("email", lambda: open_website("https://mail.google.com/mail/u/0/#inbox", "Gmail")),
    ]

    # Check simple commands
    for keyword, action in actions:
        if keyword in command or is_match(command, keyword):
            action()
            return
        
    # Handle PLAY separately
    if command.startswith("play") or is_match(command.split()[0], "play"):
        play_music(command)
        return
        
    # Exit
    if "stop" in command or "exit" in command:
        speak("Shutting down")
        os._exit(0)


    # Default fallback
    speak("I did not understand the command.")