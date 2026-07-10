import os

from dotenv import load_dotenv  # type: ignore
from groq import Groq  # pyright: ignore[reportMissingImports]

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"

prompts = ["Hi", "Tell me about time travel", "write a essay on Impact on AI on society"]

for prompt in prompts:
    message = {
        "role": "user",
        "content": prompt,
    }

    messages = [message]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
        max_tokens=100,
    )
    usage = response.usage
    print("\n")
    print(
        f"Prompt: {prompt} --> you used {usage.prompt_tokens} prompt tokens, {usage.completion_tokens} completion tokens, and {usage.total_tokens} total tokens, finish reason: {response.choices[0].finish_reason}"
    )