import os

from dotenv import load_dotenv # type: ignore
from groq import Groq # type: ignore

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

GROQ_CLIENT = Groq(api_key=API_KEY)
DEFAULT_MODEL = "openai/gpt-oss-120b"


def ask_llm(question: str, context: str, model: str = DEFAULT_MODEL) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "Answer in short or one line, answer only based on this content. "
                "Do not hallucinate. Context: "
                f"{context}"
            ),
        },
        {"role": "user", "content": question},
    ]

    response = GROQ_CLIENT.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer or ""
