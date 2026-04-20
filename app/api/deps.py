"""Injecao de dependencia da API.

Usamos um padrao simples: instancias singleton do ``LLMClient`` e do
``SessionStore`` sao criadas no startup da aplicacao (ver ``server.py``)
e expostas por estas funcoes, que o FastAPI resolve via ``Depends``.
"""

from __future__ import annotations

from fastapi import Depends, Request

from app.llm.base import LLMClient
from app.services.session_store import SessionStore


def get_llm(request: Request) -> LLMClient:
    return request.app.state.llm  # type: ignore[no-any-return]


def get_store(request: Request) -> SessionStore:
    return request.app.state.session_store  # type: ignore[no-any-return]


# Re-exportacoes para uso nas rotas.
__all__ = ["Depends", "get_llm", "get_store"]
