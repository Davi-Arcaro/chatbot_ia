"""Geracao de pergunta de quiz a partir de uma sessao."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_store
from app.api.schemas import QuizOut
from app.llm.base import LLMError
from app.services.session_store import SessionStore


router = APIRouter(prefix="/sessions/{session_id}/quiz", tags=["quiz"])


@router.post(
    "",
    response_model=QuizOut,
    status_code=status.HTTP_201_CREATED,
)
def generate_quiz(
    session_id: str,
    store: SessionStore = Depends(get_store),
) -> dict:
    record = store.get(session_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada.")

    try:
        quiz = record.bot.gerar_quiz()
    except LLMError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Falha ao gerar quiz: {exc}",
        ) from exc

    if quiz is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Nao foi possivel interpretar a resposta do modelo como quiz.",
        )
    return quiz
