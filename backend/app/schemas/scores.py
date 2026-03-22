from typing import List, Optional

from pydantic import BaseModel, Field


class ScoreItem(BaseModel):
    username: str
    time: str  # stored as "%Y-%m-%d %H:%M:%S" by backend rag/chat_engine.py
    score: str
    content: str
    total_guess: str = Field(
        description=(
            "Overall mental-health concern after enough information was collected "
        )
    )


class ScoresResponse(BaseModel):
    items: List[ScoreItem]
    username: Optional[str] = None
