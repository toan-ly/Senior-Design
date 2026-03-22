import json
from datetime import datetime
from pathlib import Path

from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.agent.openai import OpenAIAgent

from backend.utils.setup_config import load_yaml, setup_openai

from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex

from backend.app.db.session import get_db
from backend.app.models.score import Score as ScoreModel
from backend.app.models.user import User as UserModel

from backend.app.db.session import SessionLocal
from llama_index.core.postprocessor import SentenceTransformerRerank


def _read_json_file(file_path: str):
    p = Path(file_path)
    if not p.exists() or p.stat().st_size == 0:
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def load_conversation_history(conversation_file: str):
    """
    Load conversation history from disk if available, otherwise create a new chat store.
    """
    p = Path(conversation_file)
    if p.exists() and p.stat().st_size > 0:
        try:
            chat_store = SimpleChatStore.from_persist_path(conversation_file)
            print(f"✅ Loaded existing conversation from: {conversation_file}")
            return chat_store
        except json.JSONDecodeError:
            return SimpleChatStore()
    return SimpleChatStore()


def save_score(
    score: str,
    content: str,
    total_guess: str,
    username: str,
    scores_file: str,
):
    """
    Save score record to Postgres (preferred), with a JSON fallback.

    total_guess: after enough information is collected, a concise description of the
    user's overall mental-health problem (DSM-5-informed framing, not a diagnosis).
    """
    db = SessionLocal()
    try:
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if user:
            db_score = ScoreModel(
                user_id=user.id,
                score=str(score),
                content=content,
                total_guess=str(total_guess),
            )
            db.add(db_score)
            db.commit()
            db.refresh(db_score)
            print(f"💾 Score saved to Postgres for user '{username}'")
            return
        print(f"⚠️ No user '{username}' found; skipping Postgres score save")
    except Exception as exc:
        print(f"⚠️ DB score save failed: {exc}. Falling back to JSON.")
    finally:
        db.close()

    entry = {
        "username": username,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": score,
        "content": content,
        "total_guess": total_guess,
    }

    data = _read_json_file(scores_file)
    data.append(entry)
    with open(scores_file, "w") as f:
        json.dump(data, f, indent=4)
    print(f"💾 Score saved for user '{username}' in: {scores_file}")


def build_dsm5_tool(
    index,
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    reranker_top_k: int = 3,
    retrieve_k: int = 10,
    enable_hybrid: bool = False,
    hybrid_alpha: float = 0.5,
) -> QueryEngineTool:
    if enable_hybrid:
        reranker = SentenceTransformerRerank(model=reranker_model, top_n=reranker_top_k)
    else:
        reranker = None

    engine = index.as_query_engine(
        similarity_top_k=retrieve_k,
        postprocessors=[reranker],
    )

    if enable_hybrid:
        engine.vector_store_query_mode = "hybrid"
        engine.alpha = hybrid_alpha

    tool = QueryEngineTool(
        query_engine=engine,
        metadata=ToolMetadata(
            name="dsm5",
            description=(
                "Retrieves DSM-5 related information from the knowledge base. "
                "Input should be a detailed plain-text question."
            ),
        ),
    )
    return tool


def build_save_tool(scores_file: str) -> FunctionTool:
    def _save(score: str, content: str, total_guess: str, username: str):
        return save_score(
            score=score,
            content=content,
            total_guess=total_guess,
            username=username,
            scores_file=scores_file,
        )

    return FunctionTool.from_defaults(
        fn=_save,
        name="save_score",
        description=(
            "Save an assessment record after enough information has been collected. "
            "Arguments: score (string) — Poor/Average/Normal/Good; "
            "content (string) — short assessment summary; "
            "total_guess (string) — concise description of the user's overall mental-health "
            "problem in DSM-5-informed terms (symptom pattern / concern area), not a formal diagnosis; "
            "username (string) — the logged-in username."
        ),
    )


def load_prompt(
    prompt_path: str,
):
    p = Path(prompt_path)
    if not p.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return p.read_text(encoding="utf-8").strip()


def build_agent(
    username: str,
    user_info: str,
    paths_config: str = "configs/paths.yaml",
    env_path: str = "configs/secrets.env",
    token_limit: int = 3000,
    reranker_top_k: int = 3,
    retrieve_k: int = 3,
    enable_hybrid: bool = False,
    hybrid_alpha: float = 0.5,
):
    cfg = load_yaml(paths_config)
    setup_openai(env_path)

    conversation_file = cfg["chat"]["conversation_file"]
    scores_file = cfg["chat"]["scores_file"]
    system_prompt_path = cfg["prompts"]["agent_system_template"]

    storage_cfg = cfg["storage"]
    backend = storage_cfg.get("backend", "local")

    # Load conversation history
    chat_store = load_conversation_history(conversation_file)
    memory = ChatMemoryBuffer.from_defaults(
        token_limit=token_limit,
        chat_store=chat_store,
        chat_store_key=username,
    )

    if backend == "qdrant":
        # Qdrant index
        host = storage_cfg.get("host", "localhost")
        port = storage_cfg.get("port", 6333)
        collection_name = storage_cfg.get("collection_name", "mental_health_docs")

        client = QdrantClient(host=host, port=port)
        vector_store = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            enable_hybrid=enable_hybrid,
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            storage_context=storage_context,
        )
    else:
        # Fallback: local index
        index_file = cfg["storage"]["index_store"]
        storage_context = StorageContext.from_defaults(persist_dir=index_file)
        index = load_index_from_storage(
            storage_context=storage_context, index_id="vector"
        )

    # Tools
    dsm5_tool = build_dsm5_tool(
        index,
        reranker_top_k=reranker_top_k,
        retrieve_k=retrieve_k,
        enable_hybrid=enable_hybrid,
        hybrid_alpha=hybrid_alpha,
    )
    save_tool = build_save_tool(scores_file=scores_file)

    # Agent
    system_prompt_template = load_prompt(system_prompt_path)
    system_prompt = system_prompt_template.format(user_info=user_info)
    agent = OpenAIAgent.from_tools(
        tools=[dsm5_tool, save_tool],
        memory=memory,
        system_prompt=system_prompt,
    )

    return agent


def chat_once(agent, message: str) -> str:
    response = agent.chat(message)
    return str(response)


def main():
    # Example usage
    agent = build_agent(
        username="Toan Ly",
        user_info="5th year CS student at UC",
    )
    message = "I feel stressed of money and school. What should I do?"
    print(chat_once(agent, message))


if __name__ == "__main__":
    main()
