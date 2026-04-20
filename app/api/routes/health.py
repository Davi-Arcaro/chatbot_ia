"""Rota /health: exposta para checagem de liveness e status do LLM local."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_llm
from app.api.schemas import HealthOut
from app.llm.base import LLMClient
from app.llm.ollama import OllamaClient


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthOut)
def health(llm: LLMClient = Depends(get_llm)) -> HealthOut:
    model = getattr(llm, "model", "desconhecido")
    return HealthOut(
        status="ok",
        llm_reachable=llm.health(),
        llm_model=model if isinstance(model, str) else str(model),
    )
