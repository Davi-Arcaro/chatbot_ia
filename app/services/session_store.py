"""Armazenamento em memoria das sessoes de chat.

Cada sessao encapsula uma instancia de ``Chatbot`` (com historico) e a
lista de mensagens trocadas para serializacao via API. O store e
thread-safe via ``Lock``; suficiente para o unico processo uvicorn que
roda dentro do container.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from threading import Lock
from typing import Optional

from app.llm.base import LLMClient
from app.services.chatbot import Chatbot


def _now() -> datetime:
    return datetime.now(timezone.utc)


class SessionRecord:
    """Estado de uma unica sessao de chat."""

    def __init__(
        self,
        tema: str,
        llm: LLMClient,
        *,
        max_history_messages: int = 20,
        max_response_words: int = 150,
    ) -> None:
        self.id: str = str(uuid.uuid4())
        self.tema: str = tema
        self.created_at: datetime = _now()
        self.bot: Chatbot = Chatbot(
            tema,
            llm,
            max_history_messages=max_history_messages,
            max_response_words=max_response_words,
        )
        self.messages: list[dict] = []

    def append(self, role: str, content: str) -> dict:
        entry = {
            "role": role,
            "content": content,
            "created_at": _now(),
        }
        self.messages.append(entry)
        return entry

    def pop_last(self) -> None:
        if self.messages:
            self.messages.pop()

    def to_summary(self) -> dict:
        return {
            "id": self.id,
            "tema": self.tema,
            "created_at": self.created_at,
            "message_count": len(self.messages),
        }

    def to_detail(self) -> dict:
        return {
            **self.to_summary(),
            "messages": list(self.messages),
        }


class SessionStore:
    """Armazena sessoes em memoria com acesso thread-safe."""

    def __init__(
        self,
        llm: LLMClient,
        *,
        max_history_messages: int = 20,
        max_response_words: int = 150,
    ) -> None:
        self._llm = llm
        self._max_history = max_history_messages
        self._max_words = max_response_words
        self._sessions: dict[str, SessionRecord] = {}
        self._lock = Lock()

    def create(self, tema: str) -> SessionRecord:
        record = SessionRecord(
            tema,
            self._llm,
            max_history_messages=self._max_history,
            max_response_words=self._max_words,
        )
        with self._lock:
            self._sessions[record.id] = record
        return record

    def get(self, session_id: str) -> Optional[SessionRecord]:
        with self._lock:
            return self._sessions.get(session_id)

    def list_all(self) -> list[SessionRecord]:
        with self._lock:
            return sorted(
                self._sessions.values(),
                key=lambda r: r.created_at,
                reverse=True,
            )

    def delete(self, session_id: str) -> bool:
        with self._lock:
            return self._sessions.pop(session_id, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._sessions.clear()
