import os
from pathlib import Path
from dotenv import load_dotenv # type: ignore
from groq import Groq # pyright: ignore[reportMissingImports]

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)

model="qwen/qwen3.8-27b"


role="user"
prompt = "Explain the how the internet works? Also explain the OSI model of networking how it is helping the internet"
message = {"role": role, "content": prompt}

messages = [message]

stream = client.chat.completions.create(model=model, messages=messages, stream=True)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="",flush=True)
