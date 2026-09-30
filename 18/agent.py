import os
import json

from dotenv import load_dotenv # type: ignore
from groq import Groq # type: ignore
from tavily import TavilyClient # type: ignore



# SETUP

load_dotenv()

groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# Tools

def web_search(query: str) -> str:
    try:
        response = tavily.search(
            query=query,
            max_results=3,
            search_depth="basic"
        )

        results = []

        for result in response["results"]:
            results.append(
                f"Title: {result['title']}\n"
                f"URL: {result['url']}\n"
                f"Content: {result['content']}"
            )

        return "\n\n".join(results)

    except Exception as e:
        return f"Search failed: {e}"



def calculate(expression: str) -> str:
    """Perform a mathematical calculation."""

    try:
        return str(eval(expression, {"__builtins__": {}},{}))
    
    except Exception as e:
        return f"Calculation failed: {e}"



# Tool Registry

AVAILABLE_TOOLS = {
    "web_search": web_search,
    "calculate": calculate,
}



# Tool Descriptions

tools = [
    {
        "type":'function',
        "function":{

            "name": "web_search",

            "description":( # when should this function be used.
                "Search the web for current information. "
                "news, recent events, or any other information that may not be available in the model's training data. "
                "or facts that may have changed since the model's training data was collected."
            ),

            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to use for the web search."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type":'function',
        "function":{

            "name": "calculate",

            "description":( # when should this function be used.
                "Perform a mathematical calculation. "
                "This can be used for simple arithmetic, algebra."
            ),

            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to calculate. such as '2 + 2' or '3 * (4 - 1)'."
                    }
                },
                "required": ["expression"]
            }
        }
    }
]



# System Prompt

SYSTEM_PROMPT = """
You are a research assistant.

Rules:

1. Use web_search for current or changing information.
2. Use calculate for mathematical calculations.
3. You may use tools multiple times.
4. When you have enough information, answer the user.
5. Include useful source URLs from web search results.
"""

def run_agent(question:str):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for i in range(2):

        response = groq.chat.completions.create(
            model = 'openai/gpt-oss-120b',
            messages = messages,
            tools = tools,
            tool_choice = 'auto'
        )

        message = response.choices[0].message
        result = message.content
    
        messages.append(message)

        if not message.tool_calls:
            return result


        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if tool_name in AVAILABLE_TOOLS:

                tool_function = AVAILABLE_TOOLS[tool_name]
                tool_result = tool_function(**args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })
    print("\nMaximum iterations reached. Returning the last response.")


question = "What is the current population of New York City, and what is 12345 * 6789?"
answer = run_agent(question)
print(f"\nFinal Answer:\n{answer}")




