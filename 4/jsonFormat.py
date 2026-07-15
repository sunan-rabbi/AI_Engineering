import os
from pathlib import Path
from dotenv import load_dotenv # type: ignore
from groq import Groq # pyright: ignore[reportMissingImports]
from pydantic import BaseModel

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"

role = "user"
text = "Hello, I am Sunan Rabbi, Currently I am a student of Computer Science and Engineering at the RUET. I am co-founder and CTO of a tech startup. My email is sunanr@ruet.ac.bd. My contact number is +8801711111111. I am interested in AI/ML."

prompt = f"""
This is customer ticket. please extract the following information from the text: {text}
"""

message = {
    "role": role, 
    "content": prompt
}

class UserInfo(BaseModel):
    name: str
    email: str
    contact_number: str
    occupation: str
    job_title: str
    interests: str

schema = UserInfo.model_json_schema()

response_format = {
    "type": "json_object"
}

system_message = f"""
You are a helpful assistant that extracts information from customer tickets.
Please extract the following information from the text and return it in JSON format according to the provided schema
{schema}
"""

message_system = {
    "role": "system",
    "content": system_message
}

messages = [message_system, message]


response = client.chat.completions.create(model=model, messages=messages, temperature=2, response_format=response_format)

print('\n')
print("Answer: " + response.choices[0].message.content)
print('\n')