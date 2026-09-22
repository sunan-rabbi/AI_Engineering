import os
import re
from time import sleep

from dotenv import load_dotenv  # type: ignore
from groq import Groq  # type: ignore

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"


def getPriceByPhone(name):
    if name == 'iphone 18':
        return 1500
    elif name == 'iphone 17':
        return 1200
    elif name == 'sumsang s26 ultra':
        return 1350
    elif name == 'oppo reno 12A':
        return 300
    else:
        return 0

def calculator(exp):
    try:
        return eval(exp)
    except:
        return "Wrong expression"

tools = {
    "getPriceByPhone":getPriceByPhone,
    "calculator":calculator
}

systemPrompt="""
you are a shopping assistant.

you have these tools:

getPriceByPhone(name)
calculator(exp)
getPhoneByPrice(price)

IMPORTANT:
call those tool exactly like below examples:

Action: getPriceByPhone('iphone 17')
Action: calculator("5000-1000")

Never Write:

getPriceByPhone(name="iphone 17")
calculator(exp="5000 - 1000")

Follow these rules:

1. Decide what you need to do next
2. Call only one tool at a time
3. After writing an action. Stop immediately
4. Never guess or invent a tool result
5. Wait until you receive an observation
6. then decide your next action
7. when the task is complete, give final Answer

Format:

Thought: what you need to do
Action: tool_name(argument)

when you finished:

Final Answer: your answer
"""

def runAgent(question):

    message=[
        {
            "role":"system",
            "content":systemPrompt
        },
        {
            "role":"user",
            "content":question
        }
    ]

    for i in range(9):
        print("\n")
        print("Step: ", i+1)

        response=client.chat.completions.create(
            model=model,
            messages=message,
            temperature=0
        )
        answer= response.choices[0].message.content

        print(answer)

        if "Final Answer:" in answer:
            break

        match = re.search(r"Action:\s*(\w+)\((.*?)\)", answer)

        if match:

            toolName = match.group(1)
            toolInput = match.group(2)
            toolInput = toolInput.strip().strip('"').strip("'")
            
            if toolName in tools:
                tool = tools[toolName]
                observation = tool(toolInput)
            else:
                observation ='Tool not found'

            print('Observation: ', observation)

            message.append({
                "role":"assistant",
                "content":answer
            })

            message.append({
                "role":'user',
                "content":"Observation: "+ str(observation)
            })

            sleep(5)


prompt="""
I have 1500 tk, If I buy iphone 17 then how much money will I have left?
"""

runAgent(prompt)
