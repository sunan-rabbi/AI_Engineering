# Think of an LLM (Large Language Model) like talking to a smart assistant over the internet

Let's use a **restaurant analogy** first:

- **You** = Customer
- **Your App** = Waiter
- **OpenAI Server** = Kitchen
- **LLM Model** = Chef
- **API Key** = VIP membership card (proves you're allowed to order)

Now let's explain each concept.

---

## 1. API Key, Client, Server

## Client

The **client** is the application that sends a request to the AI.

Examples:

- Your website
- Mobile app
- Python script
- Node.js application

Example:

```python
from openai import OpenAI

client = OpenAI(api_key="your_api_key")
```

Here,

Your Python program is the **client**.

---

## Server

The **server** is OpenAI's computer that receives your request and generates the answer.

Flow:

```p
Your App
   │
   │ Request
   ▼
OpenAI Server
   │
   │ Response
   ▼
Your App
```

---

## API Key

An API key is like a **password** that tells OpenAI:

> "This request is coming from an authorized user."

Example:

```python
client = OpenAI(
    api_key="sk-xxxxxxxx"
)
```

Without an API key:

```=
❌ Access denied
```

With API key:

```=
✅ You can use the model
```

---

### Restaurant analogy

Customer enters restaurant.

Restaurant asks:

> "Do you have a membership card?"

Membership card = API Key

---

## 2. What is Model?

A **model** is the AI brain that generates responses.

Different models have different capabilities.

Example:

```python
model="gpt-5"
```

or

```python
model="gpt-5-mini"
```

Think of it like choosing a teacher.

```=
Math Teacher
Science Teacher
English Teacher
```

Each teacher specializes differently.

Similarly,

```=
GPT-5
GPT-5 Mini
GPT-4.1
```

Each model has different speed, cost, and capability.

Example:

```python
response = client.chat.completions.create(
    model="gpt-5",
    messages=[...]
)
```

Here you're saying:

> "Use GPT-5 to answer."

---

## 3. What is messages?

Messages are the **conversation** you send to the AI.

Example:

```python
messages=[
    {
        "role": "user",
        "content": "What is Python?"
    }
]
```

A message has two important fields:

```=
role
content
```

---

## Role = system

The system message tells the AI how it should behave.

Example:

```python
{
   "role":"system",
   "content":"You are a helpful teacher."
}
```

Meaning:

> Always behave like a teacher.

---

## Role = user

The user's question.

Example

```python
{
   "role":"user",
   "content":"Explain Python."
}
```

Meaning:

> This is what the user asked.

---

## Role = assistant

The assistant's previous answer.

Example

```python
{
   "role":"assistant",
   "content":"Python is a programming language."
}
```

This helps continue the conversation.

---

### Example conversation

```text
System:
You are a friendly teacher.

↓

User:
What is Python?

↓

Assistant:
Python is a programming language.

↓

User:
Who created it?
```

In API form:

```python
messages=[
    {
        "role":"system",
        "content":"You are a friendly teacher."
    },
    {
        "role":"user",
        "content":"What is Python?"
    },
    {
        "role":"assistant",
        "content":"Python is a programming language."
    },
    {
        "role":"user",
        "content":"Who created it?"
    }
]
```

---

## 4. What is Context?

Context means **everything the AI remembers within the current conversation** because you send it in the `messages` list.

Example:

User:

```=
My name is John.
```

Later:

```=
What is my name?
```

How does AI know?

Because the earlier message is included in the request:

```python
messages=[
   {
      "role":"user",
      "content":"My name is John."
   },
   {
      "role":"assistant",
      "content":"Nice to meet you, John."
   },
   {
      "role":"user",
      "content":"What is my name?"
   }
]
```

Without the earlier messages:

```python
messages=[
   {
      "role":"user",
      "content":"What is my name?"
   }
]
```

The AI would not know.

Think of context like the pages of a book you're currently reading. If you remove the previous pages, the story no longer makes sense.

---

## 5. What is a Token?

A token is a **small unit of text** that the model processes. It is not exactly the same as a word.

For example:

```=
Hello world
```

might become tokens like:

```=
Hello
world
```

Another example:

```=
I love programming.
```

could be split into tokens such as:

```=
I
love
program
ming
.
```

The exact tokenization depends on the model.

Approximate rule:

- 1 token ≈ ¾ of an English word
- 100 tokens ≈ 75 words

Both your input and the model's output are measured in tokens.

Example:

Input:

```=
What is Python?
```

Output:

```=
Python is a programming language.
```

The API counts tokens for both.

---

## 6. What is Response?

After sending your request, OpenAI returns a response.

Example:

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Python is a programming language."
      }
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 8,
    "total_tokens": 20
  }
}
```

---

## choices

The `choices` array contains the model's generated answer(s).

Example:

```json
"choices":[
   {
      "message":{
         "role":"assistant",
         "content":"Python is a programming language."
      }
   }
]
```

To get the text in Python:

```python
print(response.choices[0].message.content)
```

Output:

```=
Python is a programming language.
```

---

## usage

The `usage` object tells you how many tokens were used.

Example:

```json
"usage":{
   "prompt_tokens":20,
   "completion_tokens":15,
   "total_tokens":35
}
```

Meaning:

- `prompt_tokens`: tokens in your input (`messages`)
- `completion_tokens`: tokens in the AI's reply
- `total_tokens`: sum of input and output tokens

This information is useful because API costs are typically based on token usage.

---

## Complete Flow

```text
               API KEY
                  │
                  ▼
        Your Python App (Client)
                  │
                  │ Request
                  ▼
            OpenAI Server
                  │
            Uses Model (GPT-5)
                  │
         Reads Messages (Context)
                  │
          Counts Input Tokens
                  │
          Generates Response
                  │
          Counts Output Tokens
                  │
                  ▼
      Response
      ├── choices (AI answer)
      └── usage (token counts)
```

## Complete Python Example

```python
from openai import OpenAI

# Create the client using your API key
client = OpenAI(api_key="your_api_key")

# Send a conversation to the model
response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful teacher."
        },
        {
            "role": "user",
            "content": "What is Python?"
        }
    ]
)

# Read the assistant's answer
print(response.choices[0].message.content)

# See how many tokens were used
print(response.usage)
```

In this example:

- **API key** authenticates your app.
- **Client** is your Python program.
- **Server** is OpenAI's service.
- **Model** (`gpt-5`) generates the answer.
- **Messages** contain the conversation (`system` and `user`).
- **Context** is the conversation history you send.
- **Tokens** measure the size of the input and output.
- **Response** contains the AI's answer (`choices`) and token statistics (`usage`).
