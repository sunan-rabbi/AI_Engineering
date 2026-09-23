import os

from dotenv import load_dotenv  # type: ignore
from groq import Groq  # type: ignore

# Load environment variables
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"
# model = "qwen/qwen3.8-27b"


info={
    'name':'Sunan Rabbi',
    'age':'the age of sunan rabbi is 24',
    'address':'191/1 Monnafer mor, Rajshahi, Bangladesh',
    'education':'Currently study in RUET, Doing Bachelor in CSE, He is in his last semester',
    'net worth':'around 1000 dollar'
}

def getInfo(question):
    question=question.lower()

    if 'age' in question:
        return info['age']
    elif 'name' in question:
        return info['name']
    elif 'address' in question:
        return info['address']
    elif 'education' in question:
        return info['education']
    elif 'net worth' in question:
        return info['net worth']


def ask_llm(user):

    context=getInfo(user)

    sys_msg={
         "role":"system",
         "content":f"Answer in short, answer only based on this content. don't hallucinate, context: {context}"
    }

    user_msg={
         "role":"user",
         "content":user
    }

    messages=[sys_msg,user_msg]

    response = client.chat.completions.create(model=model,messages=messages)

    answer = response.choices[0].message.content

    return answer

question = "tell me sunan rabbi age"
# question = "tell me how old is sunan rabbi"

print(ask_llm(question))
