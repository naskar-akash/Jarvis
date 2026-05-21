from openai import OpenAI
import os
from dotenv import load_dotenv
import speech as sp

# Load .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_chatgpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": 
                """You are Jarvis, a smart virtual voice assistance 
                Behavior:
                    - Keep responses under 3 lines.
                    - Prioritize actions over explanations.
                    - If a command is given, confirm execution briefly.
                    - If it's a question, answer concisely.
                    - If unsure, ask a short follow-up question.
                    - Do not include unnecessary details.

                Style:
                    - Professional but friendly.
                    - Confident and assistant-like.

                Special:
                    - Do not say "As an AI model".
                    - Do not give long paragraphs unless explicitly asked.
                """},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
    
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        sp.speak("Shutting down")

    except Exception as e:
        print("ChatGPT Error:", e)
        return "Sorry, I couldn't process that."