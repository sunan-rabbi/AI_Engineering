from common import _llm_judge

def evaluate_faithfulness(groq_client, question, context, answer, model="openai/gpt-oss-120b"):
    prompt = f"""You are evaluating a RAG system.
                Question: {question}
                Retrieved Context: {context}
                Generated Answer: {answer}
                Determine whether the claims in the generated answer are supported by the retrieved context.
                Return ONLY JSON:
                {{"score": 0.0, "reason": "short explanation"}}
                Scoring:
                1.0 = All claims are supported.
                0.7 = Mostly supported with minor issues.
                0.5 = Some claims are supported.
                0.0 = Unsupported or contradictory."""
    
    result = _llm_judge(groq_client, prompt, model)
    return float(result.get("score", 0.0))


def evaluate_relevancy(groq_client, question, answer, model="openai/gpt-oss-120b"):
    prompt = f"""You are evaluating a RAG system.
                Question: {question}
                Generated Answer: {answer}
                Does the generated answer actually answer the question?
                Return ONLY JSON:
                {{"score": 0.0, "reason": "short explanation"}}
                Scoring:
                1.0 = Directly answers the question.
                0.7 = Mostly answers the question.
                0.5 = Partially answers the question.
                0.0 = Completely off-topic."""
    
    result = _llm_judge(groq_client, prompt, model)
    return float(result.get("score", 0.0))


def evaluate_correctness(groq_client, answer, ground_truth, model="openai/gpt-oss-120b"):
    prompt = f"""You are evaluating a RAG system.
                Generated Answer: {answer}
                Ground Truth Answer: {ground_truth}
                Determine whether the generated answer is factually correct compared with the ground truth.
                Return ONLY JSON:
                {{"score": 0.0, "reason": "short explanation"}}
                Scoring:
                1.0 = Completely correct.
                0.7 = Mostly correct with minor omissions.
                0.5 = Partially correct.
                0.0 = Incorrect or contradictory."""
    
    result = _llm_judge(groq_client, prompt, model)
    return float(result.get("score", 0.0))