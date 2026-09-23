# What Are Embeddings?

An **embedding** is a numerical representation of text (a word, sentence, or document) converted into a list of floating-point numbers called a **vector**.

Instead of treating words as arbitrary strings of characters, an embedding model maps text into a high-dimensional mathematical coordinate space (often hundreds or thousands of dimensions). In this coordinate space:

* Words and sentences with **similar meanings** are placed **close together**.
* Words and sentences with **unrelated meanings** are placed **far apart**.

---

## Why Do We Need Embeddings & What Problem Do They Solve?

Computers cannot inherently understand human language, nuance, or context; they only understand numbers.

## The Problem: The Flaw of Keyword Matching

In your previous script, you used keyword matching:

```python
if 'age' in question: ...

```

Keyword search breaks down immediately when a user rephrases:

* If a user asks: *"How old is Sunan?"*, keyword search fails because the word `"age"` is absent.
* If a user searches for *"automobile"*, a keyword system will miss documents talking about *"cars"*.
* If words share letters but mean different things (e.g., *"apple"* the fruit vs. *"Apple"* the company), keyword search confuses them.

## The Solution: Semantic Search

Embeddings solve the vocabulary mismatch problem. Because sentences with similar meanings produce vectors pointing in nearly the same direction, you can search by **concept** rather than identical keywords.

| Traditional Search | Embedding-Based Search |
| --- | --- |
| Matches exact letters and strings | Matches underlying meaning and intent |
| Fails on synonyms, typos, and paraphrases | Understands synonyms (*"holidays"* $\approx$ *"vacation"*) |
| Ignores sentence context | Understands context and tone |

---

### Step-by-Step Breakdown of Your Code

Your script demonstrates the two core concepts of embedding systems: **generating vector representations** and **measuring semantic similarity**.

#### 1. Loading the Embedding Model

```python
EMmodel = SentenceTransformer('all-MiniLM-L6-v2')

```

* You load a lightweight, popular open-source model from the `sentence-transformers` library.
* This model maps any piece of text into a **384-dimensional vector space**.

#### 2. Cosine Similarity Function

```python
def cosineSimilarity(a, b):
    result = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return result

```

* **Formula:**

$$\text{Cosine Similarity} = \frac{\mathbf{a} \cdot \mathbf{b}}{\Vert{}\mathbf{a}\Vert{} \Vert{}\mathbf{b}\Vert{}}$$

* **What it does:** It calculates the cosine of the angle between two vectors:
* **$1.0$** means the vectors point in the exact same direction (identical meaning).
* **$0.0$** means the vectors are orthogonal (completely unrelated).
* **$-1.0$** means the vectors point in opposite directions.
* It uses NumPy's dot product (`np.dot`) divided by the product of their vector magnitudes (`np.linalg.norm`).

#### 3. Example 1: Creating a Vector

```python
text = 'Machine learning is fun'
embedding = EMmodel.encode(text)
print(embedding[:10])

```

* `EMmodel.encode(text)` passes the string through the neural network and returns a NumPy array containing 384 floating-point numbers.
* `embedding[:10]` prints the first 10 coordinate values of that sentence in the vector space (e.g., `[-0.043, 0.082, 0.012, ...]`).

#### 4. Example 2: Comparing Semantic Meaning

```python
t1 = 'There are 24 holidays'
t2 = 'There are 24 vacation days'

v1 = EMmodel.encode(t1)
v2 = EMmodel.encode(t2)

print(cosineSimilarity(v1, v2))

```

* Even though the words `"holidays"` and `"vacation days"` are spelled completely differently, the model understands they express almost the exact same concept.
* Running `cosineSimilarity(v1, v2)` will output a very high similarity score (typically **0.85 to 0.95+**).
