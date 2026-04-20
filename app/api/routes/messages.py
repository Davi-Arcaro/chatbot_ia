"""Envio de mensagens para uma sessao existente."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_store
from app.api.schemas import MessageCreate, MessageReply
from app.llm.base import LLMError
from app.services.session_store import SessionStore


router = APIRouter(
    prefix="/sessions/{session_id}/messages",
    tags=["messages"],
)


@router.post(
    "",
    response_model=MessageReply,
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    session_id: str,
    payload: MessageCreate,
    store: SessionStore = Depends(get_store),
) -> MessageReply:
    record = store.get(session_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada.")

    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=422, detail="Mensagem vazia.")

    user_entry = record.append("user", content)

    try:
        resposta = record.bot.enviar_mensagem(content)
    except LLMError as exc:
        # Reverte a mensagem do usuario para manter consistencia com o
        # historico interno do chatbot, que nao chegou a gravar o turno.
        record.pop_last()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Falha ao obter resposta do modelo: {exc}",
        ) from exc

    bot_entry = record.append("assistant", resposta)
    return MessageReply(user_message=user_entry, bot_message=bot_entry)
