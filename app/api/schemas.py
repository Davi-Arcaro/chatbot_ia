"""Modelos Pydantic usados pelas rotas da API."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ThemeOut(BaseModel):
    id: str
    name: str


class HealthOut(BaseModel):
    status: str
    llm_reachable: bool
    llm_model: str


class SessionCreate(BaseModel):
    tema: str = Field(..., min_length=1, max_length=100)


class MessageOut(BaseModel):
    role: str
    content: str
    created_at: datetime


class SessionOut(BaseModel):
    id: str
    tema: str
    created_at: datetime
    message_count: int


class SessionDetail(SessionOut):
    messages: list[MessageOut]


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)


class MessageReply(BaseModel):
    user_message: MessageOut
    bot_message: MessageOut


class QuizOut(BaseModel):
    pergunta: str
    alternativas: dict[str, str]
    resposta: str
    explicacao: Optional[str] = ""


class ErrorOut(BaseModel):
    error: str
    detail: Optional[str] = None
