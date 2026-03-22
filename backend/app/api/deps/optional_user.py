from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from backend.app.core.security import decode_token
from backend.app.db.session import get_db
from backend.app.models.user import User

http_bearer_optional = HTTPBearer(auto_error=False)


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer_optional),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Return User if valid Bearer token is present; otherwise None (guest)."""
    if credentials is None:
        return None
    try:
        payload = decode_token(credentials.credentials)
        username: str | None = payload.get("sub")
        if username is None:
            return None
    except Exception:
        return None
    return db.query(User).filter(User.username == username).first()
