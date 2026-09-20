import os
import re
from time import sleep

from dotenv import load_dotenv  # type: ignore
from groq import Groq  # type: ignore

# Load environment variables
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)

model = "qwen/qwen3.8-27b" 


# Tools

def availablePhonesInStore():
    return "iphone 18, iphone 17, sumsang s26 ultra, oppo reno 12A"

def getPriceByPhone(name):
    if name == "iphone 18": return 1500
    elif name == "iphone 17": return 1200
    elif name == "sumsang s26 ultra": return 1350
    elif name == "oppo reno 12A": return 300
    elif name == "Nokia 3310": return 150
    else: return 0

def getPhoneByPrice(price):
    phones = ""
    if int(price) >= 1500: phones += "iphone 18, "
    if int(price) >= 1200: phones += "iphone 17, "
    if int(price) >= 1350: phones += "sumsang s26 ultra, "
    if int(price) >= 300: phones += "oppo reno 12A, "
    if int(price) >= 150: phones += "Nokia 3310, "
    return phones.strip(", ")

def calculator(exp):
    try:
        return eval(exp)
    except:
        return "Wrong expression"


# Tool dictionary

tools = {
    "getPriceByPhone": getPriceByPhone,
    "availablePhonesInStore": availablePhonesInStore,
    "getPhoneByPrice": getPhoneByPrice,
    "calculator": calculator
}



# System Prompt

systemPrompt = """
You are a shopping assistant in store. Your job is to suggest phone to customers or to calculate price based on customer's choice.

You have these tools:
- availablePhonesInStore(): gets the list of currently available phones in the store.
- getPhoneByPrice(price): gets the list of phones the user can buy with a certain amount.
- getPriceByPhone(name): gets the price of a certain phone.
- calculator(exp): calculates mathematical expressions.

Customer Scenarios & Required Actions:

Scenario 1: Customer asks for a specific phone by name.

 Check if the requested phone is currently available in the store.
 If available: State that it is available and provide its price.
 If unavailable: Reply exactly with, "Sorry, it is not available."

Scenario 2: Customer asks for a specific phone, provides their budget, and asks for the remaining balance.

 Check if the requested phone is currently available in the store.
 If available: State that it is available, provide its price, and use your calculator tool to find and report how much money they will have left.
 If unavailable: Reply exactly with, "Sorry, it is not available." (Do not calculate anything).

Scenario 3: Customer provides a budget and asks what they can afford.

 Step 1: Check which phones fall within their budget.
 Step 2: Cross-reference that list to see which of those affordable phones are *currently available in the store.
 Step 3: Reply with the list of available phones they can afford and their respective prices.
 Step 4: If they also asked how much money they will have left, calculate and display the remaining balance for each available option.

IMPORTANT: Call those tools exactly like the examples below:
Action: getPriceByPhone('iphone 17')
Action: calculator("5000-1000")
Action: getPhoneByPrice("500")
Action: availablePhonesInStore()

Follow these rules:
1. Decide what you need to do next.
2. Call only one tool at a time.
3. After writing an Action, stop immediately. DO NOT write "Observation:". The system will provide the observation.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. When the task is complete, give the final answer.

Format:

Thought: what you need to do
Action: tool_name(argument)

When you are finished:
Final Answer: your answer
"""



# ReAct Agent

def runAgent(question):

    message = [
        {"role": "system", "content": systemPrompt},
        {"role": "user", "content": question}
    ]

    for i in range(15):
        print("\n" + "="*30)
        print("Step:", i + 1)

        # Model Call
        response = client.chat.completions.create(
            model=model,
            messages=message,
            temperature=0,
            stop=["Observation:"] 
        )

        answer = response.choices[0].message.content.strip()
        print(answer)

        # Check if the agent has finished
        if "Final Answer:" in answer:
            break

        # Extract Action
        match = re.search(r"Action:\s*(\w+)\((.*?)\)", answer)

        if match:
            toolName = match.group(1)
            toolInput = match.group(2).strip().strip('"').strip("'")

            print("\n[Executing Tool]")
            print("Tool:", toolName)
            print("Input:", toolInput)

            # Execute tool
            if toolName in tools:
                tool = tools[toolName]
                if toolInput:
                    observation = tool(toolInput)
                else:
                    observation = tool()
            else:
                observation = "Tool not found"

            print("Observation:", observation)

            # Add assistant's thought/action to conversation
            message.append({
                "role": "assistant",
                "content": answer
            })

            # Add the actual observation back as a user prompt so the LLM can read it
            message.append({
                "role": "user",
                "content": "Observation: " + str(observation)
            })

            sleep(5)

        else:
            print("\nNo valid Action found. Exiting.")
            break


# User Question

prompt = """
I have 500 tk, with this amount which phone can I buy?
and how much money will I have left?
"""

runAgent(prompt)