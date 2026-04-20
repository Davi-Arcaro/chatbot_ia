"""Configuracoes da aplicacao carregadas de variaveis de ambiente.

Toda a configuracao do backend passa por este modulo. Outros modulos devem
importar ``get_settings()`` em vez de ler ``os.environ`` diretamente, para
facilitar testes e manter um unico ponto de verdade.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


# Temas educacionais pre-definidos. Mapeiam uma chave curta (usada na rota
# /api/themes e na selecao por numero no terminal) para o nome do tema.
TEMAS: dict[str, str] = {
    "1": "Biologia",
    "2": "Matematica",
    "3": "Historia",
    "4": "Fisica",
    "5": "Quimica",
    "6": "Geografia",
}


def _parse_origins(raw: str | None) -> list[str]:
    if not raw:
        return [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    return [item.strip() for item in raw.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    """Configuracao imutavel da aplicacao."""

    # --- Servidor HTTP ---
    host: str = "0.0.0.0"
    port: int = 5000

    # --- LLM local (Ollama) ---
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:1b"
    ollama_timeout: float = 120.0
    ollama_temperature: float = 0.7
    ollama_num_predict: int = 512

    # --- Chatbot ---
    max_response_words: int = 150
    max_history_messages: int = 20  # mantem contexto enxuto para LLM local

    # --- CORS ---
    cors_origins: list[str] = field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Retorna uma instancia singleton de ``Settings`` com base em env vars."""
    return Settings(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")),
        ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.2:1b"),
        ollama_timeout=float(os.getenv("OLLAMA_TIMEOUT", "120")),
        ollama_temperature=float(os.getenv("OLLAMA_TEMPERATURE", "0.7")),
        ollama_num_predict=int(os.getenv("OLLAMA_NUM_PREDICT", "512")),
        max_response_words=int(os.getenv("MAX_RESPONSE_WORDS", "150")),
        max_history_messages=int(os.getenv("MAX_HISTORY_MESSAGES", "20")),
        cors_origins=_parse_origins(os.getenv("CORS_ORIGINS")),
    )
