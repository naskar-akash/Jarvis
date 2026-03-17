# Jarvis

A simple offline voice assistant built using Python, powered by Vosk (speech recognition) and Windows Text-to-Speech.
Jarvis listens for a wake word, processes voice commands, and performs actions like opening websites or playing music.

---

## Features
- offline speech recognition using Vosk
- wake word detection
- Command execution
- Modular code structure

## Project Structure
- `main.py` — Entry point for the assistant
- `listener.py` — Handles audio input and speech recognition
- `speech.py` — Manages text-to-speech and audio output
- `command.py` — Contains command logic and execution
- `utils.py` — Utility functions
- `vosk-model-small-en-us-0.15/` — Vosk speech recognition model files
- `.env` - for environment variables
- `Readme.md`

---

## Tech Stack

- Python 3.14  
- Vosk (Speech Recognition)  
- SoundDevice (Audio Input)  
- RapidFuzz (Fuzzy Matching)  
- Windows PowerShell (Text-to-Speech)

--- 

## Installation

### 1. Clone the repository
```sh
git clone https://github.com/your-username/jarvis.git  
cd jarvis  
```
### 2. Create virtual environment
```sh
python -m venv .venv  
.venv\Scripts\activate  
```
### 3. Install dependencies
```sh
pip install vosk sounddevice rapidfuzz python-dotenv  
```
---

## Download Vosk Model

Download the model from:  
([https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models))  

Extract it and place in project folder:

`vosk-model-small-en-us-0.15/`

---

## Environment Variables

Create a `.env` file:

  WAKE_WORD=your_wake_word 

---

## Run the assistant
```sh
python main.py
```

---

## How It Works

1. Jarvis listens continuously via microphone  
2. Detects wake word (`jarvis`)  
3. Activates and listens for a command  
4. Processes command using fuzzy matching  
5. Executes action (open website, play music, etc.)  

---

## Known Issues

- May detect its own voice (feedback loop)  
- Works best with headphones 🎧  
- Windows-only TTS (PowerShell-based)  

---

## Author

 Developed by Akash Naskar
