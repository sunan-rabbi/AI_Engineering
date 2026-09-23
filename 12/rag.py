import os
from dotenv import load_dotenv  # type: ignore
from groq import Groq  # type: ignore

import numpy as np # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore

# Load environment variables
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)

AImodel = "openai/gpt-oss-120b"
# AImodel = "qwen/qwen3.8-27b"

EMmodel=SentenceTransformer('all-MiniLM-L6-v2')

docs=[
    'My name is Sunan Rabbi',
    'the age of sunan rabbi is 24',
    'currently lives in 191/1 Monnafer mor, Rajshahi, Bangladesh',
    'Currently study in RUET, Doing Bachelor in CSE, He is in his last semester',
    'net worth is around 1000 dollar'
]

docsEmbed=EMmodel.encode(docs)

def cosineSimilarity(a,b):
    result = np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return result

def retrieve(embedding):
    scores = []

    for i,doc in enumerate(docsEmbed):

        score=cosineSimilarity(embedding,doc)
        scores.append((score,docs[i]))

    scores.sort(reverse=True, key=lambda x: x[0])
    return scores[0]

def ask_llm(question,context):
 
    sys_msg={
         "role":"system",
         "content":f"Answer in short or one line , answer only based on this content. don't hallucinate, context: {context}"
    }

    user_msg={
         "role":"user",
         "content":question
    }

    messages=[sys_msg,user_msg]

    response = client.chat.completions.create(model=AImodel,messages=messages)

    answer = response.choices[0].message.content

    return answer
    

query='How old is Sunan Rabbi'
EMquery=EMmodel.encode(query)
score,context=retrieve(EMquery)
answer=ask_llm(query,context)
print(answer)