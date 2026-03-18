from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)

    scores = relationship("Score", back_populates="user", cascade="all, delete-orphan")
    messages = relationship(
        "Message", back_populates="user", cascade="all, delete-orphan"
    )
