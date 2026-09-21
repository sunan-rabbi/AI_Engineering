import os

from dotenv import load_dotenv  # type: ignore
from groq import Groq  # type: ignore

# Load environment variables
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)

model = "qwen/qwen3.8-27b" 

MainJobDescription= """
We are hiring a backend python developer.

Requirements:
1. Strong knowledge on Python or JavaScript
2. FastAPI or Express
3. PostgresSQL
4. Docker
5. AWS
6. REST APIs
7. 2+ years of experience
"""

Resume="""
Name: Sunan Rabbi

Experience:
3 years as a software Developer.

Skills:
Python,JavaScript, MongoDB, PostgreSQL, Express, REST APIs, Git

Projects:
Built a food delivery app.
Built a ticket booking site.
Built a portfolio Website.

Deployed all site in AWS using docker and github action
"""

def ask_llm(system,user):

    sys_msg={
        "role":"system",
        "content":system
    }

    user_msg={
         "role":"user",
         "content":user
    }

    messages=[sys_msg,user_msg]

    response = client.chat.completions.create(model=model,messages=messages)

    answer = response.choices[0].message.content

    return answer

def resumeExtract():
    system="""
    You are a professional HR assistant. Extract the skills from the candidates resume provided. Only return the skills no other information. Do not invent any skills by yourself 
    """

    user=f"""
    Extract the skills from this resume {Resume}
    """

    return ask_llm(system,user)

def jobDescriptionExtract():
    system="""
    You are a professional HR assistant. Extract the skills from the Job description provided. Only return the skills no other information. Do not invent any skills by yourself 
    """

    user=f"""
    Extract the skills from this {MainJobDescription}
    """

    return ask_llm(system,user)

def match(candidate,jobDescription):

    system="""
    You are a professional HR assistant. compare the skills of candidate and the skills required in the Job Description and produce a final score between 1 and 100. Also produce a short verdict whether the candidate is a good fit for the job or not
    """

    user=f"""
    Compare and match the skill, Job Description: {jobDescription} candidate skill: {candidate}
    """

    return ask_llm(system,user)

candidateSkills=resumeExtract()
jobDescription=jobDescriptionExtract()
score=match(candidateSkills,jobDescription)

print(score)