"""CRUD de sessoes de chat."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_store
from app.api.schemas import SessionCreate, SessionDetail, SessionOut
from app.llm.base import LLMError
from app.services.session_store import SessionStore


router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("", response_model=list[SessionOut])
def list_sessions(store: SessionStore = Depends(get_store)) -> list[dict]:
    return [r.to_summary() for r in store.list_all()]


@router.post(
    "",
    response_model=SessionDetail,
    status_code=status.HTTP_201_CREATED,
)
def create_session(
    payload: SessionCreate,
    store: SessionStore = Depends(get_store),
) -> dict:
    try:
        record = store.create(payload.tema.strip())
    except LLMError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Falha ao inicializar o chatbot: {exc}",
        ) from exc
    return record.to_detail()


@router.get("/{session_id}", response_model=SessionDetail)
def get_session(
    session_id: str,
    store: SessionStore = Depends(get_store),
) -> dict:
    record = store.get(session_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada.")
    return record.to_detail()


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: str,
    store: SessionStore = Depends(get_store),
) -> None:
    if not store.delete(session_id):
        raise HTTPException(status_code=404, detail="Sessao nao encontrada.")
    return None
