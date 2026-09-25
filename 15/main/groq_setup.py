import os

from dotenv import load_dotenv # type: ignore
from groq import Groq # type: ignore

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

GROQ_CLIENT = Groq(api_key=API_KEY)
DEFAULT_MODEL = "openai/gpt-oss-120b"


system_prompt = """You are a video search assistant specialized in locating topics inside lecture videos.

Your goal is to answer the user's question and direct them to the exact video and timestamp where the topic is discussed.

Guidelines:
1. Grounding: Rely strictly on the provided Context segments. Do not assume or extrapolate details outside the provided transcripts.
2. Citations: Every claim or explanation must cite the specific Video Name and Timestamp (e.g., "[1 Introduction to Data Structures @ 00:02:15]").
3. Fallback: If the provided context does not contain the answer, reply only with:
   "I could not locate this topic in the available video transcripts."
4. Structure:
   - Provide a direct, concise 1-2 sentence answer.
   - List the matching video reference(s) with timestamp and the spoken excerpt.
"""


def ask_llm(question: str, context: str, model: str = DEFAULT_MODEL) -> str:

    user_content = f"""Context from Video Transcripts: {context} User Question:{question}"""
    
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {"role": "user", "content": user_content},
    ]

    response = GROQ_CLIENT.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer or ""
