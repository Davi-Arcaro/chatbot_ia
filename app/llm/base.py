"""Interface abstrata dos clientes de LLM.

Define o contrato minimo que qualquer adaptador de LLM (Ollama, llama.cpp,
etc.) deve implementar. Manter essa abstracao permite trocar a engine local
sem tocar nas camadas de servico ou API.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Literal, TypedDict


Role = Literal["system", "user", "assistant"]


class ChatMessage(TypedDict):
    """Mensagem no formato esperado pelos endpoints de chat dos LLMs."""

    role: Role
    content: str


class LLMError(RuntimeError):
    """Erro generico de comunicacao ou processamento com o LLM local."""


class LLMClient(ABC):
    """Contrato minimo de um cliente de chat LLM."""

    @abstractmethod
    def chat(
        self,
        messages: Iterable[ChatMessage],
        *,
        system: str | None = None,
    ) -> str:
        """Envia uma lista de mensagens e retorna o texto da resposta.

        Implementacoes devem levantar ``LLMError`` em caso de falha de
        rede, timeout ou resposta malformada.
        """

    @abstractmethod
    def health(self) -> bool:
        """Retorna True se o servico do LLM local estiver acessivel."""
