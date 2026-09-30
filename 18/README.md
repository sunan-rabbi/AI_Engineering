# What is an AI Agent & How It Works

An **AI agent** is an autonomous software program powered by a Large Language Model (LLM) that can perceive its environment, make decisions, and use tools to achieve specific goals rather than just passively responding to text prompts.

An agent operates through an iterative loop:

* **Reasoning:** The LLM analyzes the user's request and determines if it needs external help.
* **Action:** Instead of just outputting text, the model generates a structured **tool call** (e.g., requesting a web search or mathematical computation).
* **Observation:** The system intercepts this call, runs the local Python function, and feeds the output back into the conversation history.
* **Completion:** The agent reviews the results and provides a final, synthesized answer.

---

## Why AI Agents Are Important

* **Bridges Limitations:** Overcomes static training data limits and mathematical inaccuracies inherent to LLMs.
* **Autonomy:** Executes multi-step workflows without requiring human intervention at every step.
* **Real-World Integration:** Connects text models directly to live data sources, calculators, APIs, and databases.

---

## Breaking Down the Code

Your script implements a minimalist ReAct (Reason + Act) loop using Groq and Tavily:

* **Setup & Tools:** Imports necessary libraries, initializes the Groq LLM client and Tavily search client, and defines native Python functions (`web_search` and `calculate`) to handle tasks the LLM cannot natively perform accurately.
* **Tool Metadata (`tools` & `AVAILABLE_TOOLS`):** Provides JSON schema definitions so the LLM understands what arguments each tool requires, mapping them to actual Python functions.
* **System Prompt:** Sets the persona ("research assistant") and establishes rules for tool usage and source citation.
* **Agent Loop (`run_agent`):** Manages a multi-turn loop (capped at 2 iterations). It sends the message history to Groq, checks if the model requested a tool call, executes the tool locally, appends the result as a `"tool"` role message, and loops back until the model finishes or reaches the limit.

This second script implements a **Classic ReAct (Reason + Act) Agent** framework, which is fundamentally different from the **Native Tool-Calling Agent** in your first script.

---

### How This Script Differs from Native Tool-Calling

| Feature | First Script (Native / API-Managed Tools) | Second Script (Classic ReAct Prompt-Managed) |
| --- | --- | --- |
| **How Tools are Defined** | Passed to the LLM via structured JSON schemas (`tools = [...]`). | Described directly in plain text inside the `systemPrompt`. |
| **How Tools are Triggered** | The LLM provider (Groq) natively intercepts and returns structured object data (`message.tool_calls`). | The LLM writes plain text following a strict pattern (`Action: tool_name(arg)`). |
| **How Actions are Extracted** | Automatically handled by the API response object. | Extracted manually using regular expressions (`re.search`) on the text output. |
| **Handling Observations** | The framework manages internal `"tool"` role message objects. | The framework appends the observation back as a simulated `"user"` message. |
| **Model Constraints** | Works with any model that supports native function calling. | Relies heavily on prompt engineering and strict stopping criteria (`stop=["Observation:"]`). |

---

### Deep Dive Into the ReAct Mechanics

#### 1. The ReAct Loop Pattern

ReAct stands for **Reasoning and Acting**. Instead of letting the model guess everything at once or rely purely on its training memory, it forces a cycle:

* **Thought:** The model analyzes the current state and decides what step is missing.
* **Action:** It writes out a specific text command to invoke a tool.
* **Stop Generation:** The code uses `stop=["Observation:"]` so the model cuts itself off *before* it tries to hallucinate what the tool's output would be.
* **Observation:** Your Python code intercepts the text, runs the function, and injects the result back into the chat history as a user message.

#### 2. Prompt Engineering as a Compiler

Because this script doesn't use the provider's native tool API, the **System Prompt** acts as the programming interface:

* It defines explicit scenarios and step-by-step logic ("Scenario 3: Step 1, Step 2...").
* It provides concrete syntax examples (`Action: getPhoneByPrice("500")`) so the model knows the exact text format to output.

#### 3. Manual Parsing with Regular Expressions

In `runAgent`, python looks for the text pattern using regex:

```python
match = re.search(r"Action:\s*(\w+)\((.*?)\)", answer)

```

If the model writes `Action: getPhoneByPrice("500")`, the regex captures `getPhoneByPrice` as the tool name and `500` as the input argument, executes it locally in Python, and feeds the result back.

---

### Which Approach is Better?

* **Native Tool-Calling (First Script):** More robust, less prone to syntax errors, cleaner code, and natively supported by modern LLM APIs.
* **Classic ReAct (Second Script):** Great for educational purposes, highly transparent (you can read every thought and action stream in plain text), and works on models that do not support native function-calling APIs.
