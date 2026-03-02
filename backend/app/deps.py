from backend.rag.chat_engine import build_agent, chat_once
from typing import Dict, Any
from threading import Lock

_AGENT_CACHE: Dict[str, Any] = {}
_LOCK = Lock()


def get_or_create_agent(session_id: str, user_info: str):
    sid = session_id.strip()
    if not sid:
        raise ValueError("Session ID cannot be empty.")

    key = sid.lower()
    with _LOCK:
        if key in _AGENT_CACHE:
            return _AGENT_CACHE[key]

        agent = build_agent(username=sid, user_info=user_info)
        _AGENT_CACHE[key] = agent
        return agent


def run_chat(session_id: str, user_info: str, message: str) -> str:
    agent = get_or_create_agent(session_id, user_info)
    return chat_once(agent, message)
