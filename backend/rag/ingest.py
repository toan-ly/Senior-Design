from pathlib import Path
from typing import Optional

from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.extractors import SummaryExtractor
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

from backend.utils.setup_config import load_config, setup_openai


def load_prompt(
    prompt_path: str,
) -> str:
    prompt_file = Path(prompt_path)
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return prompt_file.read_text(encoding="utf-8").strip()


def load_cache(
    cache_file: str,
):
    cache_path = Path(cache_file)
    if cache_path.exists() and cache_path.is_file():
        print(f"Cache file found: {cache_file}. Loading cache...")
        return IngestionCache.from_persist_path(cache_file)
    print("No cache found. Starting fresh ingestion...")
    return None


def persist_cache(
    pipeline: IngestionPipeline,
    cache_file: str,
):
    Path(cache_file).parent.mkdir(parents=True, exist_ok=True)
    if pipeline.cache:
        pipeline.cache.persist(persist_path=cache_file)
        print(f"💾 Cache saved: {cache_file}")


def build_pipeline(
    summary_prompt: str,
    cache: Optional[IngestionCache],
    chunk_size: int = 512,
    chunk_overlap: int = 20,
) -> IngestionPipeline:
    pipeline = IngestionPipeline(
        transformations=[
            TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap),
            SummaryExtractor(summaries=["self"], prompt_template=summary_prompt),
            OpenAIEmbedding(),
        ],
        cache=cache,
    )
    return pipeline


def ingest_docs(
    paths_config: str = "configs/paths.yaml",
    rag_config: str = "configs/dev.yaml",
    env_path: str = "configs/secrets.env",
):
    cfg = load_config(paths_file=paths_config, rag_config_file=rag_config)
    setup_openai(env_path)

    # LLM config
    Settings.llm = OpenAI(
        model=cfg["llm"]["model"], temperature=cfg["llm"]["temperature"]
    )

    input_files = cfg["data"]["raw"]
    cache_file = cfg["ingestion"]["cache_file"]
    summary_prompt_path = cfg["prompts"]["summary_extract"]

    chunk_size = cfg["chunking"]["chunk_size"]
    chunk_overlap = cfg["chunking"]["chunk_overlap"]

    # Load docs
    docs = SimpleDirectoryReader(
        input_files=input_files,
        filename_as_id=True,
    ).load_data()

    if not docs:
        raise RuntimeError("No documents loaded! Check configs/paths.yaml")

    for doc in docs:
        print(f"Loaded document: {doc.get_doc_id()}")

    # Load prompt and cache
    summary_prompt = load_prompt(summary_prompt_path)
    cache = load_cache(cache_file)

    # Run ingestion pipeline
    pipeline = build_pipeline(
        summary_prompt, cache, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    nodes = pipeline.run(documents=docs)
    persist_cache(pipeline, cache_file)

    print(f"✅ Ingestion done. Nodes: {len(nodes)}")

    return nodes


if __name__ == "__main__":
    ingest_docs()
