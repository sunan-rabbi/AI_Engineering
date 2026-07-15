# All Import
import os
from pathlib import Path
from dotenv import load_dotenv # type: ignore
from groq import Groq # pyright: ignore[reportMissingImports]
from pydantic import BaseModel
from pypdf import PdfReader
import json


# Load Essential Environment Variables and File
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

reader = PdfReader("./SunanResume.pdf")
client = Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"


# Parse the PDF and Extract Text
text =''
for page in reader.pages:
    text += page.extract_text() + "\n"



# user Prompt
role = "user"

prompt = f"""
This is a resume of Applicant for a job opening. please extract the following information from the text: {text}
"""

message = {
    "role": role, 
    "content": prompt
}


# Response Format and Schema Definition
class experience(BaseModel):
    company_name: str
    job_title: str
    start_date: str
    end_date: str
    responsibilities: str
    work_details: str

class projects(BaseModel):
    project_name: str
    project_description: str
    technologies_used: str
    project_link: str

class UserInfo(BaseModel):
    name: str
    email: str
    contact_number: str
    github_link: str
    experience: list[experience]
    projects: list[projects]
    education: str
    awards: str
    extracurricular_activities: str
    interests: str
    match_rate: str

schema = UserInfo.model_json_schema()

response_format = {
    "type": "json_object"
}


# System Prompt

job_requirements = f"""
**Junior Web Developer (MERN / Next.js / PostgreSQL)**

### Requirements

* Basic knowledge of the MERN stack (MongoDB, Express.js, React.js, Node.js).
* Familiarity with Next.js and PostgreSQL.
* Understanding of REST APIs, HTML, CSS, JavaScript (ES6+), and Git.
* At least **6 months of hands-on experience** through internships, freelance work, or real-world projects.
* Experience working on **real-life web applications** from development to deployment.
* Ability to collaborate effectively in a team environment using Git/GitHub.
* Strong problem-solving skills and eagerness to learn new technologies.
* Good communication skills and a positive attitude.

### Nice to Have

* Experience with TypeScript.
* Basic knowledge of authentication (JWT/OAuth).
* Familiarity with deployment platforms such as Vercel, Render, or Docker.
* Portfolio or GitHub profile showcasing personal or team projects.
"""

system_message = f"""
You are a helpful HR assistant that extracts information from applicant resumes.
Please extract the following information from the text and return it in valid JSON format according to the provided schema not any markdown, in match_rate provide a percentage match rate based on the job requirements {job_requirements} and the applicant's qualifications.
{schema}
"""

message_system = {
    "role": "system",
    "content": system_message
}


# Final Messages and API Call
messages = [message_system, message]

response = client.chat.completions.create(model=model, messages=messages, temperature=0, response_format=response_format)


# Validate the Response and Save to JSON
finalResponse = response.choices[0].message.content

try:
    user = UserInfo.model_validate_json(finalResponse)
    with open("output.json", "w") as f:
        json.dump(user.model_dump(), f, indent=4)

except Exception as e:
    print("Error validating the response:", e)
    print("Response received:", finalResponse)