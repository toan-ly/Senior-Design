from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.api.deps.current_user import get_current_user
from backend.app.api.deps.optional_user import get_optional_current_user
from backend.app.db.session import get_db
from backend.app.models.message import Message as MessageModel
from backend.app.models.user import User
from backend.app.schemas.chat import (
    ChatHistoryResponse,
    ChatHistoryMessage,
    ChatRequest,
    ChatResponse,
)
from backend.app.core.chat_service import run_chat

router = APIRouter(tags=["chat"])


def _persist_exchange(
    db: Session,
    user: User,
    session_id: str,
    user_message: str,
    assistant_message: str,
) -> None:
    sid = (session_id or "")[:100]
    db.add(
        MessageModel(
            user_id=user.id,
            session_id=sid,
            role="user",
            content=user_message,
        )
    )
    db.add(
        MessageModel(
            user_id=user.id,
            session_id=sid,
            role="assistant",
            content=assistant_message,
        )
    )
    db.commit()


@router.get("/v1/chat/history", response_model=ChatHistoryResponse)
def get_chat_history(
    session_id: str = Query(..., min_length=1, max_length=100),
    limit: int = Query(200, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return the most recent `limit` messages for this user and session (oldest first)."""
    rows = (
        db.query(MessageModel)
        .filter(
            MessageModel.user_id == current_user.id,
            MessageModel.session_id == session_id[:100],
        )
        .order_by(MessageModel.created_at.desc())
        .limit(limit)
        .all()
    )
    rows.reverse()
    return ChatHistoryResponse(
        messages=[ChatHistoryMessage(role=r.role, content=r.content) for r in rows]
    )


@router.post("/v1/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    try:
        response = run_chat(
            session_id=request.session_id,
            user_info=request.user_info or "",
            message=request.message,
        )
        if current_user is not None:
            try:
                _persist_exchange(
                    db,
                    current_user,
                    request.session_id,
                    request.message,
                    response,
                )
            except Exception as persist_exc:
                # Do not fail the chat if persistence fails
                print(f"⚠️ Chat history save failed: {persist_exc}")
        return ChatResponse(response=response, meta={"session_id": request.session_id})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
