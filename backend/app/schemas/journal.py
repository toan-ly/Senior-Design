from typing import Optional

from pydantic import BaseModel


class JournalEntryIn(BaseModel):
    username: str
    date: str  # "YYYY-MM-DD"
    mood: str
    journal_text: str
    reflection_text: Optional[str] = None


class JournalEntryOut(JournalEntryIn):
    pass


class JournalMonthResponse(BaseModel):
    month: str  # "YYYY-MM"
    items: list[JournalEntryOut]
