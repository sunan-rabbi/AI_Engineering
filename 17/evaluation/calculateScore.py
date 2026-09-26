from checkContext import context_precision, context_recall
from checkAnswer import evaluate_faithfulness, evaluate_relevancy, evaluate_correctness
from common import golden_dataset

def run_evaluation(results,context,answer, groq_client, model="openai/gpt-oss-120b"):
    
    all_scores = {
        "precision": [],
        "recall": [],
        "faithfulness": [],
        "relevancy": [],
        "correctness": []
    }

    for test in golden_dataset:
        question = test["question"]
        ground_truth = test["ground_truth"]

        # 3. Score Calculations
        precision = context_precision(groq_client, question, results, model)
        recall = context_recall(groq_client, question, context, ground_truth, model)
        faithfulness = evaluate_faithfulness(groq_client, question, context, answer, model)
        relevancy = evaluate_relevancy(groq_client, question, answer, model)
        correctness = evaluate_correctness(groq_client, answer, ground_truth, model)

        all_scores["precision"].append(precision)
        all_scores["recall"].append(recall)
        all_scores["faithfulness"].append(faithfulness)
        all_scores["relevancy"].append(relevancy)
        all_scores["correctness"].append(correctness)

    # 5. Final Summary
    for metric, values in all_scores.items():
        average = sum(values) / len(values) if values else 0.0
        print(f"{metric.capitalize():20}: {average:.2f}")