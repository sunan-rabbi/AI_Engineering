# 1. What is the System Role?

The **system role** gives the AI its **instructions before the conversation starts**.

Think of it as setting the AI's **personality, behavior, or job**.

## Real-life example

Imagine you ask three different people the same question:

**Question:**

> Explain Python.

### Person 1: Teacher

They answer:

> Python is a programming language used for web development, AI, automation, and more.

### Person 2: Comedian

They answer:

> Python isn't just a snake—it also writes code faster than I write jokes!

### Person 3: Doctor

They answer:

> I'm a doctor, so programming isn't my specialty.

The **question is the same**, but the **role changes the answer**.

The system message works the same way.

---

Every answer will follow that instruction unless a later instruction overrides it.

---

## 2. What is Temperature?

**Temperature controls how random or creative the AI's answers are.**

Think of it as a **creativity knob**.

```#
Temperature
0 ------------------------ 2

Less Creative         More Creative
```

* Low temperature → More focused and consistent
* High temperature → More varied and imaginative

---

## Temperature = 0

The AI tries to give the most predictable answer.

```python
temperature = 0
```

User:

> What is the capital of France?

Response:

> Paris.

Ask again:

> Paris.

Ask again:

> Paris.

Almost always the same.

---

## Temperature = 0.3

A little creativity.

User:

> Describe a cat.

Possible responses:

> A cat is a small, playful pet.

or

> Cats are curious animals known for their independence.

Both are similar.

---

## Temperature = 1

More creative.

User:

> Describe a cat.

Possible responses:

* A tiny tiger that rules your house.
* A furry companion that loves naps.
* A curious explorer with silent footsteps.

---

## When should you use different temperatures?

| Task                   | Recommended Temperature | Why                  |
| ---------------------- | ----------------------- | -------------------- |
| Math                   | 0–0.2                   | Consistent answers   |
| Coding                 | 0–0.3                   | Predictable code     |
| Technical explanations | 0.2–0.5                 | Clear and reliable   |
| Blog writing           | 0.7                     | More engaging        |
| Story writing          | 0.8–1.2                 | Creative ideas       |
| Poetry                 | 1.0+                    | Imaginative language |

---

Here:

* **Model** → `gpt-5` (the AI being used)
* **System role** → "You are a friendly programming teacher." (how the AI should behave)
* **User role** → "Explain Python." (the user's request)
* **Temperature** → `0.7` (moderately creative, not too random)

---

## Quick Summary

| Concept            | Simple Meaning                                    | Example                               |
| ------------------ | ------------------------------------------------- | ------------------------------------- |
| **System Role**    | Tells the AI **how to behave**                    | "You are a teacher."                  |
| **User Role**      | The user's question                               | "Explain Python."                     |
| **Assistant Role** | The AI's previous reply                           | "Python is a programming language."   |
| **Temperature**    | Controls **how creative or random** the answer is | `0` = consistent, `1` = more creative |

A useful way to remember it is:

* **System role = "Who are you?"**
* **User role = "What should you do?"**
* **Temperature = "How creative should you be while doing it?"**
