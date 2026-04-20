"""Aplicacao FastAPI do chatbot educacional.

Executa com::

    uvicorn app.api.server:app --host 0.0.0.0 --port 5000

As dependencias (``LLMClient`` e ``SessionStore``) sao instanciadas no
evento de startup e ficam disponiveis em ``app.state``. Isso permite que
as rotas as obtenham via ``Depends(get_llm)`` / ``Depends(get_store)``
sem construirem o cliente a cada request.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, messages, quiz, sessions, themes
from app.core.config import get_settings
from app.llm.ollama import OllamaClient
from app.services.session_store import SessionStore


logger = logging.getLogger("chatbot.api")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    llm = OllamaClient(
        base_url=settings.ollama_url,
        model=settings.ollama_model,
        timeout=settings.ollama_timeout,
        temperature=settings.ollama_temperature,
        num_predict=settings.ollama_num_predict,
    )
    store = SessionStore(
        llm,
        max_history_messages=settings.max_history_messages,
        max_response_words=settings.max_response_words,
    )
    app.state.llm = llm
    app.state.session_store = store
    app.state.settings = settings

    logger.info(
        "Backend iniciado | ollama_url=%s model=%s",
        settings.ollama_url,
        settings.ollama_model,
    )
    if not llm.health():
        logger.warning(
            "Servico Ollama indisponivel em %s. O backend subiu mesmo assim; "
            "as rotas retornarao 502 ate o Ollama estar pronto.",
            settings.ollama_url,
        )
    try:
        yield
    finally:
        llm.close()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Chatbot Eliane API",
        version="2.0.0",
        description=(
            "API REST do chatbot educacional. Usa um LLM local via Ollama, "
            "sem dependencia de servicos externos."
        ),
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Prefixo /api para alinhar com VITE_API_URL do frontend.
    app.include_router(health.router, prefix="/api")
    app.include_router(themes.router, prefix="/api")
    app.include_router(sessions.router, prefix="/api")
    app.include_router(messages.router, prefix="/api")
    app.include_router(quiz.router, prefix="/api")

    return app


app = create_app()
