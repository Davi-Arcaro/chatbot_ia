"""Rota somente-leitura dos temas pre-definidos."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.schemas import ThemeOut
from app.core.config import TEMAS


router = APIRouter(prefix="/themes", tags=["themes"])


@router.get("", response_model=list[ThemeOut])
def list_themes() -> list[ThemeOut]:
    return [ThemeOut(id=key, name=name) for key, name in TEMAS.items()]
