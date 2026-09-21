# **Prompt chaining**

In your script, the goal is to evaluate whether a candidate fits a job. Instead of dumping the full raw resume and job description into one massive prompt, the script executes a **3-stage chain**:

```diagram
[Raw Resume]          ──> (Call 1: resumeExtract)         ──> [candidateSkills]   ──┐
                                                                                    ├──> (Call 3: match) ──> [Final Score & Verdict]
[Raw Job Description] ──> (Call 2: jobDescriptionExtract) ──> [jobDescription]    ──┘

```

---

## Step-by-Step Breakdown of Your Chain

### 1. Stage 1: Extraction & Isolation (Parallel Steps)

* **Chain Link 1 (`resumeExtract()`):**
* **Input:** Full raw `Resume` text (contains names, experience years, project descriptions, AWS/Docker deployment details).
* **Transformation:** Filters out non-skill text (names, company history, fluff) and returns only isolated skills.
* **Output:** Stored in `candidateSkills`.

* **Chain Link 2 (`jobDescriptionExtract()`):**
* **Input:** Full raw `MainJobDescription` text.
* **Transformation:** Filters out company intro, job title, and non-skill requirements, returning strictly the required skills.
* **Output:** Stored in `jobDescription`.

### 2. Stage 2: Synthesis & Evaluation (Convergent Step)

* **Chain Link 3 (`match(candidateSkills, jobDescription)`):**
* **Input:** Takes the two refined strings generated in Stage 1 (`candidateSkills` and `jobDescription`).
* **Transformation:** Compares only the cleanly extracted skills against each other, calculates a score (1–100), and issues a hiring verdict.
* **Output:** The final evaluation printed to the terminal.

---

### Why Prompt Chaining is Better Than a Single Prompt

* **Reduces Cognitive Load & Hallucinations:** Large Language Models can suffer from "lost in the middle" phenomena when given too much unstructured data at once. Pre-filtering the raw text removes noise, letting the final scoring step focus on an exact, 1-to-1 comparison.
* **Modularity and Debugging:** If the final match score feels incorrect, you can easily inspect `candidateSkills` and `jobDescription` separately to see which step failed (e.g., did it fail to extract Docker from the project notes, or did it fail at the scoring logic?).
* **Token & Cost Efficiency in Production:** In a production pipeline, job descriptions rarely change. By decoupling the steps, you could extract the job requirements once, cache `jobDescription`, and only run the resume extraction and match steps for every new applicant
