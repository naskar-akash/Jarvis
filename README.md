# Jarvis

Jarvis is a Python-based voice assistant project. It leverages speech recognition and command execution to provide a hands-free assistant experience.

## Features
- Speech recognition using Vosk
- Command execution
- Modular code structure

## Project Structure
- `main.py` — Entry point for the assistant
- `listener.py` — Handles audio input and speech recognition
- `speech.py` — Manages text-to-speech and audio output
- `command.py` — Contains command logic and execution
- `utils.py` — Utility functions
- `vosk-model-small-en-us-0.15/` — Vosk speech recognition model files

## Requirements
- Python 3.7+
- [Vosk](https://alphacephei.com/vosk/)

## Setup
1. Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```
2. Install dependencies:
   ```sh
   pip install vosk
   ```
3. Download and extract the Vosk model to the `vosk-model-small-en-us-0.15/` directory if not already present.

## Usage
Run the assistant:
```sh
python main.py
```

## License
MIT License
