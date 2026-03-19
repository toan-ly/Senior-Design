import os
from typing import Any, Dict, Optional

import requests


API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")


def register_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    full_name: Optional[str] = None,
) -> Dict[str, Any]:
    response = requests.post(
        f"{API_BASE}/v1/auth/register",
        json={
            "username": username,
            "password": password,
            "email": email,
            "full_name": full_name,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def login_user(username: str, password: str) -> Dict[str, Any]:
    # FastAPI's OAuth2PasswordRequestForm expects form-encoded data
    response = requests.post(
        f"{API_BASE}/v1/auth/login",
        data={"username": username, "password": password},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_current_user(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        f"{API_BASE}/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def send_chat_message(
    session_id: str,
    user_info: str,
    message: str,
    access_token: Optional[str] = None,
) -> str:
    headers: Dict[str, str] = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    response = requests.post(
        f"{API_BASE}/v1/chat",
        json={
            "session_id": session_id,
            "user_info": user_info,
            "message": message,
        },
        headers=headers or None,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["response"]


def get_scores(
    username: str,
    access_token: Optional[str] = None,
) -> Any:
    """
    Fetch saved health scores for a user from backend.
    """
    headers: Dict[str, str] = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    response = requests.get(
        f"{API_BASE}/v1/scores",
        params={"username": username},
        headers=headers or None,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_journal_month(
    username: str,
    month: str,
    access_token: Optional[str] = None,
) -> Any:
    headers: Dict[str, str] = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    response = requests.get(
        f"{API_BASE}/v1/journal/month",
        params={"username": username, "month": month},
        headers=headers or None,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def upsert_journal_entry(
    username: str,
    date: str,
    mood: str,
    journal_text: str,
    reflection_text: Optional[str] = None,
    access_token: Optional[str] = None,
) -> Any:
    headers: Dict[str, str] = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    response = requests.post(
        f"{API_BASE}/v1/journal/entry",
        json={
            "username": username,
            "date": date,
            "mood": mood,
            "journal_text": journal_text,
            "reflection_text": reflection_text,
        },
        headers=headers or None,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
