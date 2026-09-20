# Best Prompt Structure

A well-structured prompt helps an AI understand **who it should act as, what it needs to do, what rules it must follow, and how the final answer should look**.

A useful prompt structure is:

1. **Role**
2. **Task**
3. **Constraints**
4. **Output Format**
5. **Zero-shot / One-shot**
6. **Fallback**

## 1. Role

Define **who the AI should act as** or what expertise it should use.

It gives the AI the necessary context and perspective for completing the task.

**Example:**

> You are an experienced Python instructor who teaches programming to university students.

## 2. Task

Clearly state **what you want the AI to do**.

The task should be specific and actionable rather than vague.

**Example:**

> Explain the concept of Object-Oriented Programming and provide three simple Python examples.

## 3. Constraints

Specify **rules, limitations, requirements, or things the AI should avoid**.

Constraints can include length, language, difficulty level, sources, coding style, or prohibited content.

**Example:**

> Use simple English. Keep the explanation suitable for a beginner. Do not use advanced Python features.

**Purpose:**

* Controls the scope of the answer
* Prevents unwanted content
* Makes the response more consistent with your requirements

---

## 4. Output Format

Tell the AI **how the final answer should be structured or presented**.

You can specify headings, tables, bullet points, code blocks, JSON, Markdown, etc.

**Example:**

> Format the answer in Markdown using headings, bullet points, and Python code blocks.

---

## 5. Zero-shot / One-shot

This specifies whether you provide **an example of the desired output**.

### Zero-shot

Give the instruction **without providing an example**.

**Example:**

> Explain recursion in Python using a simple example.

The AI has to understand the desired task from the instructions alone.

### One-shot

Give **one example** to demonstrate what you want.

**Example:**

> Explain concepts using this format:
>
> **Concept:** Encapsulation
> **Definition:** Hiding internal implementation details.
> **Example:** A class with private attributes.
>
> Now explain **Inheritance** using the same format.

**Purpose:**

* **Zero-shot:** Useful for straightforward tasks.
* **One-shot:** Useful when you want a specific style, structure, or behavior.

---

## 6. Fallback

Specify **what the AI should do if the requested task cannot be completed or necessary information is missing**.

This prevents the AI from making assumptions or inventing information.

**Example:**

> If the required information is missing, ask me for it instead of making assumptions.

Another example:

> If you cannot find reliable information, clearly state that the information could not be verified.
