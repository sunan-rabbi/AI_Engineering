# What is Chunking?

**Chunking** is the process of breaking down a large text document, article, or video transcript into smaller, manageable pieces (called "chunks") before converting them into vector embeddings and storing them in a database.

* **Analogy:** Imagine trying to memorize an entire 500-page textbook by reading it all as a single sentence. You wouldn't remember anything. Instead, you read it **chapter by chapter, paragraph by paragraph**. Chunking does the exact same thing for AI.

---

## Why is Chunking Needed?

Chunking is a critical step in any RAG (Retrieval-Augmented Generation) pipeline for several major reasons:

### 1. Embedding Model Limits (Token Constraints)

Embedding models (like `all-MiniLM-L6-v2` or OpenAI's models) have strict input limits (often 256 or 512 tokens). If you try to pass an entire 5-page PDF or a 30-minute video transcript as a single piece of text, the embedding model will cut it off, throw an error, or fail to process it.

### 2. Avoiding "Diluted" Meanings (Semantic Precision)

If a single chunk contains five completely different topics, its vector embedding becomes a "mushy average" of all those topics.

* If a user asks a specific question about *Topic C*, a giant chunk containing Topics A through E will only have a mediocre similarity score.
* By breaking text into smaller chunks, each chunk stays **laser-focused on a single idea**, ensuring high vector similarity scores when searched.

### 3. Preventing LLM Distraction (Noise Reduction)

Even though modern LLMs have large context windows (like 128k tokens), giving them massive walls of irrelevant text introduces **noise**.

* If you hand an LLM a huge transcript chunk just to answer a simple question, it can get distracted, miss the detail, or hallucinate.
* Small, precise chunks give the LLM exactly what it needs—nothing more, nothing less.

### 4. Precise Citations (Like Your Video Timestamps)

In your video project, chunking is what allows you to pinpoint the **exact second** a speaker said something. If a video was treated as one single 10-minute chunk, your system could only tell the user *"It's somewhere in Video 1"*. By chunking the transcript every few seconds, you can say *"It's at timestamp 00:02:15"*.

---

### Common Chunking Strategies

* **Fixed-size chunking:** Splitting text every $X$ characters or words (e.g., every 300 words).
* **Semantic/Sentence chunking:** Splitting text naturally by sentences or paragraphs (which is essentially what Whisper did automatically when it outputted your video transcript segments!)
