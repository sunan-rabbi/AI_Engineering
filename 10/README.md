# What is RAG and Why Do We Need It?

**Retrieval-Augmented Generation (RAG)** is an AI technique that combines information retrieval with text generation.

* **The Problem It Solves:** Large Language Models (LLMs) are trained on massive public datasets, but they **do not know private data** (like company files, personal records, or real-time news), and they can **hallucinate** (make things up) when they don't know an answer. Fine-tuning an LLM to learn new data is expensive and slow.
* **Why We Need It:** RAG acts as an "open-book exam" for the AI. Instead of forcing the model to rely solely on its memory, you fetch the exact facts required and hand them to the model right when it answers a question.
* **How It Helps:** It ensures answers are accurate, grounded in real facts, completely up-to-date, and secure without needing to retrain the underlying model.

---

## What is a "Classic, Simplified" RAG?

A **simplified RAG** strips away the complex infrastructure typically used in production (such as vector databases, embedding models, and semantic chunking) and reduces the architecture down to its bare-bones logic:

1. **The Source:** A small dictionary or list of text.
2. **The Retrieval:** Simple keyword or rule-based matching.
3. **The Generation:** Injecting that text into a strict prompt template.

---

### Step-by-Step Breakdown of Your Code

Your script is a textbook example of this simplified workflow, split into three clear phases:

#### 1. The Knowledge Base (The Source)

```python
info = {
    'name': 'Sunan Rabbi',
    'age': 'the age of sunan rabbi is 24',
    ...
}

```

* **What it does:** This acts as your private database. In an advanced system, this would be thousands of pages stored in a vector DB; here, it is a simple Python dictionary containing raw facts about Sunan Rabbi.

#### 2. The Retrieval Step (`getInfo`)

```python
def getInfo(question):
    question = question.lower()
    if 'age' in question:
        return info['age']
    elif 'name' in question:
        return info['name']
    # ...

```

* **What it does:** When a user asks a question, this function scans for keywords (like `"age"` or `"name"`). Instead of a complex mathematical similarity search, it uses simple Python conditional logic to **retrieve** the exact matching value from your dictionary.

#### 3. Augmentation & Generation (`ask_llm`)

```python
    context = getInfo(user)

    sys_msg = {
        "role": "system",
        "content": f"Answer in short, answer only based on this content. don't hallucinate, context: {context}"
    }
    
    messages = [sys_msg, user_msg]
    response = client.chat.completions.create(model=model, messages=messages)

```

* **Augmentation:** You take the retrieved text (`context`) and merge it directly into the system prompt with strict instructions (*"answer only based on this content. don't hallucinate"*).
* **Generation:** You pass these enriched messages to Groq (`openai/gpt-oss-120b`). The model reads your context and translates it into a polished, natural-sounding response.
