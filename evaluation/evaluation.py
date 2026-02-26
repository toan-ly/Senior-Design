import asyncio
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import nest_asyncio
from typing import List

from llama_index.core import Settings
from llama_index.core.evaluation import (
    BatchEvalRunner,
    CorrectnessEvaluator,
    FaithfulnessEvaluator,
    RelevancyEvaluator,
)
from llama_index.core.llama_dataset.generator import RagDatasetGenerator
from llama_index.llms.openai import OpenAI

from backend.utils.setup_config import setup_openai
from backend.rag.index import build_vector_index
from backend.rag.ingest import ingest_docs


CONFIG_PATH = "configs/paths.yaml"
ENV_PATH = "configs/secrets.env"


def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def generate_questions(
    nodes,
    num_questions_per_chunk: int = 1,
):
    """
    Generate evaluation questions from the given nodes for RAG evaluation.
    """
    generator = RagDatasetGenerator(
        nodes,
        num_questions_per_chunk=num_questions_per_chunk,
    )
    eval_questions_df = generator.generate_questions_from_nodes()
    return eval_questions_df.to_pandas()


async def run_eval(
    query_engine,
    queries: List[str],
):
    runner = BatchEvalRunner(
        {
            "correctness": CorrectnessEvaluator(),
            "faithfulness": FaithfulnessEvaluator(),
            "relevancy": RelevancyEvaluator(),
        },
        show_progress=True,
    )

    return await runner.aevaluate_queries(queries=queries, query_engine=query_engine)


def results_to_df(questions_df, eval_result):
    rows = []
    queries = questions_df["query"].tolist()

    for i, query in enumerate(queries):
        c = eval_result["correctness"][i]
        f = eval_result["faithfulness"][i]
        r = eval_result["relevancy"][i]

        rows.append(
            {
                "query": query,
                "correctness_response": c.response,
                "correctness_score": c.score,
                "correctness_passing": c.passing,
                "correctness_feedback": c.feedback,
                "faithfulness_response": f.response,
                "faithfulness_score": f.score,
                "faithfulness_passing": f.passing,
                "faithfulness_feedback": f.feedback,
                "relevancy_response": r.response,
                "relevancy_score": r.score,
                "relevancy_passing": r.passing,
                "relevancy_feedback": r.feedback,
            }
        )

    return pd.DataFrame(rows)


def compute_average(df):
    return {
        "correctness_avg": df["correctness_score"].mean(),
        "faithfulness_avg": df["faithfulness_score"].mean(),
        "relevancy_avg": df["relevancy_score"].mean(),
    }


def main():
    nest_asyncio.apply()

    # Config setup
    # cfg = load_paths_config(CONFIG_PATH)
    setup_openai(ENV_PATH)
    Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.2)

    # Ingest
    nodes = ingest_docs(
        paths_config=CONFIG_PATH,
        env_path=ENV_PATH,
    )

    # Build index and query engine
    index = build_vector_index(
        nodes=nodes,
        paths_config=CONFIG_PATH,
    )
    query_engine = index.as_query_engine(similarity_top_k=3)

    # Generate eval questions
    print("Generating evaluation questions...")
    questions_df = generate_questions(nodes, num_questions_per_chunk=1)

    out_dir = Path("evaluation/results") / timestamp()
    out_dir.mkdir(parents=True, exist_ok=True)
    questions_path = out_dir / "eval_questions.csv"
    questions_df.to_csv(questions_path, index=False)
    print(f"✅ Evaluation questions saved to: {questions_path}")

    # Run evaluation
    queries = questions_df["query"].tolist()
    eval_result = asyncio.run(run_eval(query_engine, queries))

    # Save results
    results_df = results_to_df(questions_df, eval_result)
    results_path = out_dir / "eval_results.csv"
    results_df.to_csv(results_path, index=False)
    print(f"✅ Evaluation results saved to: {results_path}")

    # Compute and print averages
    averages = compute_average(results_df)
    print("Average Scores:")
    print(f"Correctness Average: {averages['correctness_avg']:.4f}")
    print(f"Faithfulness Average: {averages['faithfulness_avg']:.4f}")
    print(f"Relevancy Average: {averages['relevancy_avg']:.4f}")
    print("✅ Evaluation completed!")

    with open(out_dir / "averages.json", "w") as f:
        json.dump(averages, f, indent=4)


if __name__ == "__main__":
    main()
