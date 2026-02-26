import json
from datetime import datetime
from pathlib import Path

from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.agent.openai import OpenAIAgent

from src.utils.setup_config import load_paths_config, setup_openai


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
    Save score record to JSON file
    """
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


def build_dsm5_tool(index, top_k: int = 3):
    engine = index.as_query_engine(similarity_top_k=top_k)
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
    """
    Wrap save_score with scores_file bound in closure so the agent doesn't need to pass it.
    """

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
            "Save an assessment record. "
            "Arguments: score (string), content (string), total_guess (string), username (string)."
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
    top_k: int = 3,
):
    cfg = load_paths_config(paths_config)
    setup_openai(env_path)

    conversation_file = cfg["chat"]["conversation_file"]
    scores_file = cfg["chat"]["scores_file"]
    index_file = cfg["storage"]["index_store"]
    system_prompt_path = cfg["prompts"]["agent_system_template"]

    # Load conversation history
    chat_store = load_conversation_history(conversation_file)
    memory = ChatMemoryBuffer.from_defaults(
        token_limit=token_limit,
        chat_store=chat_store,
        chat_store_key=username,
    )

    # Load vector index
    storage_context = StorageContext.from_defaults(persist_dir=index_file)
    index = load_index_from_storage(storage_context=storage_context, index_id="vector")

    # Tools
    dsm5_tool = build_dsm5_tool(index, top_k=top_k)
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
