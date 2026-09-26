from common import _llm_judge


def context_precision(groq_client, question, retrieved_docs, model="openai/gpt-oss-120b"):
    if not retrieved_docs:
        return 0.0

    relevant_chunks = 0
    for doc in retrieved_docs:
        chunk = doc.payload.get("text", "")
        prompt = f"""You are evaluating the retrieval quality of a RAG system.
                Question: {question}
                Retrieved chunk: {chunk}
                Is this chunk relevant to answering the question?
                Return ONLY JSON:
                {{"relevant": true, "reason": "short explanation"}}
                Return true if the chunk contains information that is useful for answering the question. 
                Return false if it is unrelated."""
        
        result = _llm_judge(groq_client, prompt, model)
        if result.get("relevant", False):
            relevant_chunks += 1

    return relevant_chunks / len(retrieved_docs)


def context_recall(groq_client, question, context, ground_truth, model="openai/gpt-oss-120b"):
    prompt = f"""You are evaluating the retrieval quality of a RAG system.
            Question: {question}
            Ground Truth Answer: {ground_truth}
            Retrieved Context: {context}
            Does the retrieved context contain enough information to produce the ground truth answer?
            Return ONLY JSON:
            {{"score": 0.0, "reason": "short explanation"}}
            Scoring:
            1.0 = All important information needed for the answer is present.
            0.7 = Most important information is present, but some details are missing.
            0.5 = Some important information is present.
            0.0 = The required information is absent."""
    
    result = _llm_judge(groq_client, prompt, model)
    return float(result.get("score", 0.0))