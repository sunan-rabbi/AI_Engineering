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
role="user"
prompt = "Write a short poem about One piece."
message = {"role": role, "content": prompt}
messages = [message]

response = client.chat.completions.create(model=model, messages=messages)
print(response)

print('\n\n')
print("Answer: " + response.choices[0].message.content)