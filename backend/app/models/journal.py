from sqlalchemy import Column, Date, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.app.db.session import Base


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    mood = Column(String(50), nullable=False)
    journal_text = Column(Text, nullable=False)
    reflection_text = Column(Text, nullable=True)

    user = relationship("User")

    __table_args__ = (UniqueConstraint("user_id", "date", name="uq_journal_user_date"),)
