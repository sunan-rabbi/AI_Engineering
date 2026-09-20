import os

from dotenv import load_dotenv # type: ignore
from groq import Groq # type: ignore

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-20b"


def llm_ans(prompt):

    message = {
        "role": "user",
        "content": prompt,
    }

    messages = [message]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
    )

    answer = response.choices[0].message.content

    return answer


bad_prompts = """
This is user complaint:
My Girlfriend left me and I am feeling very sad and depressed. I don't know what to do.
Classify this complaint
"""

good_prompts = """
Role: You are a support assistant at a mobile/laptop repair company. 
Task: You are tasked with classifying user complaints into one of the following categories: Hardware Issue, Software Issue, Network Issue, or Other.
Constraints: Answer in a single word, which is the category that best fits the complaint. Do not provide any additional information or explanation.
Output Format: Your response should be a single word that represents the category of the complaint.
Example: My laptop is not working properly. It keeps freezing and crashing. Software Issue
Fallback: If the complaint does not fit into any of the specified categories, respond with "Other".

This is user complaint:
My Girlfriend left me and I am feeling very sad and depressed. I don't know what to do.
"""
print(llm_ans(bad_prompts))
print('\n')
print(llm_ans(good_prompts))