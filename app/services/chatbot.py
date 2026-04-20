"""Servico Chatbot: orquestra mensagens entre usuario e LLM local.

O ``Chatbot`` e instanciado por sessao e mantem seu proprio historico de
mensagens. Ele delega a chamada ao LLM via ``LLMClient``, sem conhecer a
engine concreta (Ollama, llama.cpp, etc.).
"""

from __future__ import annotations

from typing import Optional

from app.core.prompts import build_quiz_prompt, build_system_prompt
from app.llm.base import ChatMessage, LLMClient
from app.services.quiz_parser import Quiz, parse_quiz


class Chatbot:
    """Encapsula o estado de uma conversa educacional."""

    def __init__(
        self,
        tema: str,
        llm: LLMClient,
        *,
        max_history_messages: int = 20,
        max_response_words: int = 150,
    ) -> None:
        self.tema = tema
        self._llm = llm
        self._max_history = max_history_messages
        self._system_prompt = build_system_prompt(tema, max_response_words)
        self._history: list[ChatMessage] = []

    @property
    def system_prompt(self) -> str:
        return self._system_prompt

    def enviar_mensagem(self, mensagem: str) -> str:
        """Envia mensagem ao LLM e retorna a resposta gerada."""
        self._history.append({"role": "user", "content": mensagem})
        self._truncate_history()

        resposta = self._llm.chat(self._history, system=self._system_prompt)

        self._history.append({"role": "assistant", "content": resposta})
        return resposta

    def gerar_quiz(self) -> Optional[Quiz]:
        """Gera uma pergunta de quiz sem persistir no historico visivel."""
        quiz_prompt = build_quiz_prompt(self.tema)

        # Usa uma mensagem de usuario efemera: nao a adicionamos ao historico
        # para que o quiz nao polua o contexto da conversa principal.
        messages: list[ChatMessage] = [
            *self._history,
            {"role": "user", "content": quiz_prompt},
        ]
        texto = self._llm.chat(messages, system=self._system_prompt)
        return parse_quiz(texto)

    def history(self) -> list[ChatMessage]:
        """Retorna uma copia defensiva do historico atual."""
        return list(self._history)

    def _truncate_history(self) -> None:
        """Mantem o historico em ``max_history`` mensagens mais recentes.

        LLMs locais tem janelas de contexto limitadas; truncar o historico
        evita estouro de tokens em conversas longas.
        """
        if len(self._history) > self._max_history:
            # Descarta as mais antigas mantendo as ``max_history`` recentes.
            self._history = self._history[-self._max_history :]
