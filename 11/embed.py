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

def cosineSimilarity(a,b):
    result = np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return result


# Example 1

text = 'Machine learning is fun'

embedding=EMmodel.encode(text)

print('\n')
print(embedding[:10])
print()


# Example 2

t1 = 'There are 24 holidays'
t2 = 'There are 24 vacation days'

v1=EMmodel.encode(t1)
v2=EMmodel.encode(t2)

print(cosineSimilarity(v1,v2))
