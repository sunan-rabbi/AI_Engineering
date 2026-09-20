# Understanding the ReAct (Reasoning + Acting) Framework in AI

## 1. What is ReAct?

**ReAct** stands for **Reasoning + Acting**.

Introduced by researchers from Google Research and Princeton in late 2022, it is a prompting and control design pattern that allows Large Language Models (LLMs) to solve complex problems by intertwining two capabilities:

1. **Reasoning (Thought):** The model thinks step-by-step about what to do next.
2. **Acting (Action):** The model performs an action in the outside world (like querying a database, searching the web, or running a Python script).

Before ReAct, LLMs either tried to answer everything purely from internal memory (leading to hallucinations) or used tools blindly without planning. ReAct bridges this gap by creating an interactive, back-and-forth loop.

---

## 2. The Core Loop: Thought, Action, Observation

The ReAct pattern works in an iterative cycle known as the **ReAct Loop**:

```diagram

User Query
│
▼
┌─────────────────────────────────┐
│ 1. Thought (Reasoning)          │ <───┐
│    "What should I do next?"     │     │
└────────────────┬────────────────┘     │
│                      │
▼                      │
┌─────────────────────────────────┐     │
│ 2. Action (Decision)            │     │
│    "Call Tool X with input Y"   │     │
└────────────────┬────────────────┘     │
│                      │
▼                      │
┌─────────────────────────────────┐     │
│ [External Python Code Executes] │     │
└────────────────┬────────────────┘     │
│                      │
▼                      │
┌─────────────────────────────────┐     │
│ 3. Observation (Perception)     │     │
│    "Tool X returned result Z"   │ ────┘
└────────────────┬────────────────┘
│
▼ (When enough info is gathered)
┌─────────────────────────────────┐
│ 4. Final Answer                 │
└─────────────────────────────────┘

```

### The Three Steps Defined

1. **Thought:** The model generates internal reasoning. It verbalizes what it knows, what it is missing, and what strategy to follow.
2. **Action:** The model emits a structured command targeting a specific tool with defined arguments (e.g., `getPriceByPhone('iphone 17')`).
3. **Observation:** The execution environment (your Python code) intercepts the action, runs the corresponding function, and injects the result back into the prompt conversation as context for the model.

---

## 3. How ReAct Works in Your Python Code

Here is the exact lifecycle of how your script executes a ReAct request:

### Step 1: Instructing via System Prompt

You supply the LLM with a strict contract defining:

- The tools it can access
- The formatting syntax (`Thought:`, `Action:`, `Final Answer:`).
- The instruction to pause immediately after outputting an `Action`.

### Step 2: The Model's Turn

When the user asks:
> *"I have 500 tk, with this amount which phone can I buy and how much money will I have left?"*

The model evaluates the prompt and outputs:

```text
Thought: I need to check which phones are available in the store first.
Action: availablePhonesInStore()

```

### Step 3: Interception by Python

Because you set `stop=["Observation:"]`, the LLM halts generation. Your Python script then:

1. Catches the string `availablePhonesInStore()`.
2. Matches it with regex: `re.search(r"Action:\s*(\w+)\((.*?)\)", text)`.
3. Runs the real Python function: `tools["availablePhonesInStore"]()`.
4. Obtains the output: `"iphone 18, iphone 17, sumsang s26 ultra, oppo reno 12A"`.

### Step 4: Feeding the Observation

Your script appends the tool output to the message history:

```python
message.append({
    "role": "user", 
    "content": "Observation: iphone 18, iphone 17, sumsang s26 ultra, oppo reno 12A"
})

```

### Step 5: Next Iteration

Now seeing the observation, the model starts the next cycle:

```text
Thought: Now I need to see which phones cost 500 tk or less.
Action: getPhoneByPrice("500")

```

This loop repeats until the model determines it has all the data required to answer the query, concluding with:

```text
Final Answer: You can buy the oppo reno 12A for 300 tk. You will have 200 tk left.

```

---

## 4. Why ReAct Is Important

| Traditional LLM Approach | ReAct Agent Approach |
| --- | --- |
| **Guesses facts:** Relies purely on static training weights. | **Inspects reality:** Uses real-time tools (APIs, databases, calculators). |
| **Black box:** You cannot see why or how it arrived at an answer. | **Transparent:** Every `Thought` exposes the reasoning trajectory. |
| **Poor arithmetic:** Token prediction frequently fails at multi-digit math. | **Offloaded math:** Delegated to deterministic tools (Python `eval` / math libraries). |
| **Hallucinates answers:** Invents inventory or prices when unsure. | **Grounded:** Confined strictly to returned `Observation` values. |

---

## 5. Common ReAct Pitfalls & How to Avoid Them

- **Hallucinated Observations:** If the LLM is not instructed with a stop token (e.g., `stop=["Observation:"]`), it will continue writing text, making up fake tool results on its own instead of waiting for your code.

- **Infinite Loops:** If a tool returns unexpected data or an error, the agent may get stuck repeating the same `Action`. Always safeguard with a `max_steps` loop count (like your `range(15)`).

- **Malformed Tool Calls:** Free-form text prompts can result in slight syntax deviations (e.g., missing quotes or adding extra spaces). Strict regex patterns or native **Function Calling / Tool Use** APIs help prevent parsing errors.
