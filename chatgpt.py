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
                {"role": "system", "content": "You are Jarvis, a virtual assistance who is enable to provide short but important responoses within three or four lines"},
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