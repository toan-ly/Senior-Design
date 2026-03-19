from datetime import date, datetime
import calendar
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.journal import JournalEntry as JournalEntryModel
from backend.app.models.user import User as UserModel
from backend.app.schemas.journal import (
    JournalEntryIn,
    JournalEntryOut,
    JournalMonthResponse,
)


router = APIRouter(tags=["journal"])


def _parse_date(date_str: str) -> date:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="date must be YYYY-MM-DD") from exc


@router.post("/v1/journal/entry")
def upsert_entry(entry_in: JournalEntryIn, db: Session = Depends(get_db)):
    entry_date = _parse_date(entry_in.date)

    user = db.query(UserModel).filter(UserModel.username == entry_in.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    existing = (
        db.query(JournalEntryModel)
        .filter(
            JournalEntryModel.user_id == user.id, JournalEntryModel.date == entry_date
        )
        .first()
    )

    if existing:
        existing.mood = entry_in.mood
        existing.journal_text = entry_in.journal_text
        existing.reflection_text = entry_in.reflection_text
    else:
        db.add(
            JournalEntryModel(
                user_id=user.id,
                date=entry_date,
                mood=entry_in.mood,
                journal_text=entry_in.journal_text,
                reflection_text=entry_in.reflection_text,
            )
        )

    db.commit()
    return {"ok": True, "date": entry_in.date}


@router.get("/v1/journal/month", response_model=JournalMonthResponse)
def list_month(
    username: str = Query(min_length=1),
    month: str = Query(min_length=7, description="YYYY-MM"),
    db: Session = Depends(get_db),
):
    # month validation: YYYY-MM
    try:
        month_dt = datetime.strptime(month, "%Y-%m")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="month must be YYYY-MM") from exc

    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        return JournalMonthResponse(month=month, items=[])

    year = month_dt.year
    month_num = month_dt.month
    last_day = calendar.monthrange(year, month_num)[1]
    start = date(year, month_num, 1)
    end = date(year, month_num, last_day)

    rows = (
        db.query(JournalEntryModel)
        .filter(
            JournalEntryModel.user_id == user.id,
            JournalEntryModel.date >= start,
            JournalEntryModel.date <= end,
        )
        .order_by(JournalEntryModel.date.desc())
        .all()
    )

    items: List[JournalEntryOut] = []
    for r in rows:
        items.append(
            JournalEntryOut(
                username=username,
                date=r.date.strftime("%Y-%m-%d"),
                mood=r.mood,
                journal_text=r.journal_text,
                reflection_text=r.reflection_text,
            )
        )

    return JournalMonthResponse(month=month, items=items)
