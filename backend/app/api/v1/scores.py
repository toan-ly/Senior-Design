from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.score import Score as ScoreModel
from backend.app.models.user import User as UserModel
from backend.app.schemas.scores import ScoreItem, ScoresResponse


router = APIRouter(tags=["scores"])


@router.get("/v1/scores", response_model=ScoresResponse)
def get_scores(
    username: Optional[str] = Query(default=None, min_length=1),
    db: Session = Depends(get_db),
):
    """
    Return scores stored in Postgres.
    If `username` is provided, filter to that user.
    """
    query = db.query(ScoreModel, UserModel.username).join(
        UserModel, ScoreModel.user_id == UserModel.id
    )
    if username:
        query = query.filter(UserModel.username == username)

    rows = query.order_by(ScoreModel.created_at.desc()).all()

    items: List[ScoreItem] = []
    for score_row, username_row in rows:
        created_at: datetime = score_row.created_at
        items.append(
            ScoreItem(
                username=username_row,
                time=created_at.strftime("%Y-%m-%d %H:%M:%S"),
                score=str(score_row.score),
                content=score_row.content,
                total_guess=str(score_row.total_guess),
            )
        )

    return ScoresResponse(items=items, username=username)
