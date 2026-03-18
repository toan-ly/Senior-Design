from fastapi import APIRouter, HTTPException
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.core.chat_service import run_chat

router = APIRouter(tags=["chat"])


@router.post("/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        response = run_chat(
            session_id=request.session_id,
            user_info=request.user_info,
            message=request.message,
        )
        return ChatResponse(response=response, meta={"session_id": request.session_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
