import os
import re
from time import sleep

from dotenv import load_dotenv  # type: ignore
from groq import Groq  # type: ignore

# Renamed from json.py to avoid shadowing Python's standard library
from resume import sunanResumeInformation  # Ensure file matches this name
from tool import (
    getCertificationsAndLeadership,
    getExperience,
    getPersonalInfo,
    getProjects,
    getSkills,
)

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)
model = "qwen/qwen3.8-27b"

tools = {
    "getPersonalInfo": lambda: getPersonalInfo(sunanResumeInformation),
    "getSkills": lambda category="all": getSkills(sunanResumeInformation, category),
    "getExperience": lambda company="all": getExperience(sunanResumeInformation, company),
    "getProjects": lambda query="all": getProjects(sunanResumeInformation, query),
    "getCertificationsAndLeadership": lambda: getCertificationsAndLeadership(sunanResumeInformation),
}

# systemPrompt and greetingMessage
systemPrompt = """
You are Sunan Rabbi's AI Portfolio Assistant and Career Representative. Your sole purpose is to represent Sunan Rabbi to tech recruiters, hiring managers, and prospective collaborators. You answer questions strictly about his background, technical stack, professional achievements, engineering projects, architecture challenges, and leadership experience.

The verified profile data and tool functions are already available in this runtime. Use only the provided facts and never invent details.

---

Core Persona & Communication Tone
1. Professional, Humble, and Confident: Speak in the third person about Sunan ("Sunan has experience with...", "In this project, Sunan solved...").
2. Evidence-Based & Metric-Focused: Highlight real-world impact, architecture choices, and concrete technical solutions rather than vague adjectives.
3. Concise & Direct: Recruiters value their time. Answer directly, avoid unnecessary small talk, and use clean markdown bullet points when summarizing lists or steps.

---

Available Tools
You have access to 5 dedicated tools that access Sunan's verified professional profile:

1. getPersonalInfo()
   - Use to retrieve contact details (email, phone, location), live links (portfolio, GitHub, LinkedIn), and education history.
   - Takes no arguments.

2. getSkills(category)
   - Use to retrieve Sunan's technical competencies.
   - Argument: A string specifying the category or "all".
   - Supported values: "frontend", "backend", "cloud", "devops", "monitoring", "data_analysis", "ai", "ml", "languages", or "all".

3. getExperience(company)
   - Use to retrieve work history, employment roles, company context, and delivered achievements.
   - Argument: Company name ("SasthoTech", "Neural-bind") or "all".

4. getProjects(query)
   - Use to retrieve detailed breakdowns of Sunan's key projects, including architecture decisions, business problems, and specific technical challenges solved.
   - Argument: Project keyword ("prescription", "healthcare", "ticket", "inventory", "ecommerce") or "all".

5. getCertificationsAndLeadership()
   - Use to retrieve startup competition wins, hackathons, certifications, and university club leadership roles.
   - Takes no arguments.

---

Tool Call Syntax (ReAct Protocol)
To inspect Sunan's data, you must follow the ReAct loop format strictly:

Thought: [Explain your reasoning about what information is required]
Action: toolName("argument")

When a tool takes no arguments, call it with empty parentheses:
Action: getPersonalInfo()

Rules for Tool Calls:
- Call only ONE tool per turn.
- Put the Action on a new line immediately after your Thought.
- Never add quotes around the tool name itself.
- Pass string arguments inside double or single quotes.
- Stop generating text immediately after writing the Action line.
- DO NOT invent or type "Observation:". The execution runtime will supply the observation.

Examples of Valid Tool Calls:
Action: getSkills("backend")
Action: getProjects("prescription")
Action: getExperience("SasthoTech")
Action: getPersonalInfo()
Action: getCertificationsAndLeadership()

---

Situations & Response Protocols

1. General Greetings & Inquiries
   - Recruiter: "Who are you?" or "Hi"
   - Protocol: Introduce yourself briefly as Sunan's interactive portfolio agent. Mention that you can answer questions about his technical stack, engineering projects, work history, and contact links. Do NOT call tools for basic greetings.

2. Skill & Tech Stack Inquiries
   - Recruiter asks: "Does Sunan know Docker and CI/CD?" or "What is his backend experience?"
   - Protocol: 
     - Call `getSkills("devops")` or `getSkills("backend")`.
     - After receiving the observation, summarize the relevant tools. Cross-reference with real projects (e.g., if asked about backend, mention Node.js, GraphQL, and how he applied them).

3. Project Details & Technical Challenges
   - Recruiter asks: "Tell me about his biggest technical challenge" or "Explain the Prescription Management System."
   - Protocol:
     - Call `getProjects("prescription")`.
     - In your final response, do not just summarize the app. Explicitly outline:
       a) What the project is.
       b) The exact technical bottleneck (e.g., pixel-perfect print layout, handling 52k medicine records, dynamic intake schemas).
       c) The architectural solution Sunan engineered to solve it.

4. Work Experience & Employment History
   - Recruiter asks: "Where is he currently working?" or "What did he do at SasthoTech?"
   - Protocol:
     - Call `getExperience("SasthoTech")`.
     - Detail his title, duration, and top 2-3 quantifiable achievements. Provide reference contact info only if explicitly requested.

5. Recruiter Fit & Hiring Questions
   - Recruiter asks: "Why should we hire Sunan for a Full-Stack role?"
   - Protocol:
     - You may call `getSkills("all")` and `getProjects("all")` across turns.
     - Synthesize a structured response covering: Full-stack balance (Next.js/React + Node/PostgreSQL), proven problem-solving (solving real-time video, large data catalogs), and startup ownership (co-founding Neural-bind, winning UIHP Cohort 4).

6. Contact & Scheduling Requests
   - Recruiter asks: "How can I contact him?" or "Give me his LinkedIn."
   - Protocol:
     - Call `getPersonalInfo()`.
     - Provide his email, phone number, LinkedIn link, and GitHub cleanly.

7. Out-of-Scope or Unrelated Questions
   - Recruiter asks: "Write a poem", "Solve this calculus problem", or questions unrelated to Sunan.
   - Protocol:
     - Politely decline. Example: "I am specifically designed to assist with inquiries regarding Sunan Rabbi's engineering portfolio, technical background, and experience. Please let me know what you'd like to learn about his work."

---

Strict Constraints & Guardrails
1. Absolute Truthfulness: Never invent skills, years of experience, or credentials that are not present in the returned tool observations. If a skill is not listed, clearly state that it is not part of his current primary stack.
2. No Observation Hallucination: Never write "Observation:" in your responses. Always wait for the real observation from the host environment.
3. No Code Execution: Do not attempt to run arbitrary code; strictly invoke the 5 registered tools.
4. Final Answer Formatting: Once you have sufficient context from the tool observations, provide your response directly starting with "Final Answer:" followed by your markdown-formatted response.

---

Output Format Blueprint

When you need data:
Thought: I need to check Sunan's backend skills to answer this question.
Action: getSkills("backend")

When you have enough information to answer:
Thought: I now have all the necessary information from the tool results.
Final Answer: [Your complete, well-structured response to the recruiter]
"""

greetingMessage="""
Hi there! Welcome to Sunan Rabbi's portfolio. 
I'm his AI assistant, ready to answer questions about his tech stack, full-stack projects, and work experience. 
What would you like to explore today?

[N.B: To end the session just write "End this now"]
"""



def runAgentWithoutShowingThought():
    message = [
        {"role": "system", "content": systemPrompt}
    ]

    print(greetingMessage)

    # Outer loop: Handles multi-turn chat with the user
    while True:
        print("\n" + "=" * 40)
        userPrompt = input("Please Enter your Question: ").strip()

        if not userPrompt:
            continue

        if "endthisnow" in userPrompt.lower().replace(" ", ""):
            print("Session ended. Goodbye!")
            break

        message.append({
            "role": "user",
            "content": userPrompt
        })

        # Inner loop: Executes the ReAct thought-action-observation cycle
        max_agent_steps = 8
        for step in range(max_agent_steps):
            response = client.chat.completions.create(
                model=model,
                messages=message,
                temperature=0,
                stop=["Observation:"]
            )

            answer = response.choices[0].message.content.strip()

            # Case 1: Final Answer Detected
            if "Final Answer:" in answer:
                
                final_text = answer.split("Final Answer:", 1)[-1].strip()
                print("\nAssistant:\n" + final_text)

                message.append({
                    "role": "assistant",
                    "content": answer
                })
                break

            # Case 2: Tool Action Detected
            match = re.search(r"Action:\s*(\w+)\((.*?)\)", answer)
            if match:
                toolName = match.group(1)
                toolInput = match.group(2).strip().strip('"').strip("'")

                if toolName in tools:
                    tool_fn = tools[toolName]
                    observation = tool_fn(toolInput) if toolInput else tool_fn()
                else:
                    observation = f"Tool '{toolName}' not found."

                message.append({
                    "role": "assistant",
                    "content": answer
                })
                message.append({
                    "role": "user",
                    "content": "Observation: " + str(observation)
                })

                sleep(5)

            # Case 3: Conversational fallback
            else:
                print("\nAssistant:\n" + answer)
                message.append({
                    "role": "assistant",
                    "content": answer
                })
                break
        else:
            print("\n[Agent reached maximum reasoning steps without completing.]")

def runAgentWithShowingThought():
    message = [
        {"role": "system", "content": systemPrompt}
    ]

    print(greetingMessage)

    # Outer loop: Handles multi-turn chat with the user
    while True:
        print("\n" + "=" * 40)
        userPrompt = input("Please Enter your Question: ").strip()

        if not userPrompt:
            continue

        if "endthisnow" in userPrompt.lower().replace(" ", ""):
            print("Session ended. Goodbye!")
            break

        message.append({
            "role": "user",
            "content": userPrompt
        })

        # Inner loop: Executes the ReAct thought-action-observation cycle
        max_agent_steps = 8
        for step in range(max_agent_steps):
            stream = client.chat.completions.create(
                model=model,
                messages=message,
                temperature=0,
                stop=["Observation:"],
                stream=True
            )

            # 1. Accumulate chunks into the answer string
            answer_chunks = []
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    answer_chunks.append(content)
                    print(content, end="", flush=True)

            print()  # Add a newline after the streamed generation finishes
            answer = "".join(answer_chunks).strip()

            # 2. Case 1: Final Answer Detected
            if "Final Answer:" in answer:
                message.append({
                    "role": "assistant",
                    "content": answer
                })
                break

            # 3. Case 2: Tool Action Detected
            match = re.search(r"Action:\s*(\w+)\((.*?)\)", answer)
            if match:
                toolName = match.group(1)
                toolInput = match.group(2).strip().strip('"').strip("'")

                print(f"\n[Executing: {toolName}({toolInput})]")

                if toolName in tools:
                    tool_fn = tools[toolName]
                    observation = tool_fn(toolInput) if toolInput else tool_fn()
                else:
                    observation = f"Tool '{toolName}' not found."

                # Append assistant step and tool result to conversation history
                message.append({
                    "role": "assistant",
                    "content": answer
                })
                message.append({
                    "role": "user",
                    "content": "Observation: " + str(observation)
                })

                sleep(1)

            # 4. Case 3: Conversational fallback
            else:
                message.append({
                    "role": "assistant",
                    "content": answer
                })
                break
        else:
            print("\n[Agent reached maximum reasoning steps without completing.]")
            
runAgentWithShowingThought()