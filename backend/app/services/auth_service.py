import sqlite3
from pathlib import Path
from typing import Any


class AuthService:
    """Small SQLite-backed auth service for local development and testing."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = Path(db_path or "auth.db")
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    name TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS refresh_tokens (
                    token TEXT PRIMARY KEY,
                    email TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def signup(self, email: str, password: str, name: str) -> dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO users (email, password, name) VALUES (?, ?, ?)",
                (email, password, name),
            )
            conn.commit()
        return {"email": email, "name": name}

    def login(self, email: str, password: str) -> dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT email FROM users WHERE email = ? AND password = ?",
                (email, password),
            ).fetchone()

        if row is None:
            raise ValueError("invalid credentials")

        access_token = f"access-{email}"
        refresh_token = f"refresh-{email}"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO refresh_tokens (token, email) VALUES (?, ?)", (refresh_token, email))
            conn.commit()

        return {"access_token": access_token, "refresh_token": refresh_token}

    def refresh(self, refresh_token: str) -> dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT email FROM refresh_tokens WHERE token = ?", (refresh_token,)).fetchone()

        if row is None:
            raise ValueError("invalid refresh token")

        return {"access_token": f"access-{row[0]}"}
