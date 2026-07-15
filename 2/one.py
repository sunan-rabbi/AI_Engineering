import os
from pathlib import Path
from dotenv import load_dotenv # type: ignore
from groq import Groq # pyright: ignore[reportMissingImports]

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"

message = {
    "role": "user", 
    "content": "I Love you!"
}

message_system = {
    "role": "system",
    "content": "You are my girlfriend."
}

messages = [message_system, message]

response = client.chat.completions.create(model=model, messages=messages, temperature=0.5)

print('\n')
print("Answer: " + response.choices[0].message.content)
print('\n')