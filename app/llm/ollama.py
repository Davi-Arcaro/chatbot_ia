"""Cliente HTTP para o servico Ollama (LLM local).

O Ollama expoe uma API HTTP em ``http://localhost:11434`` por padrao. Este
modulo encapsula as duas rotas que utilizamos: ``/api/chat`` para geracao
de texto com historico de mensagens e ``/api/tags`` para checagem de saude.

Referencia: https://github.com/ollama/ollama/blob/main/docs/api.md
"""

from __future__ import annotations

import logging
from typing import Iterable

import httpx

from app.llm.base import ChatMessage, LLMClient, LLMError


logger = logging.getLogger(__name__)


class OllamaClient(LLMClient):
    """Adaptador para o servico Ollama rodando localmente."""

    def __init__(
        self,
        base_url: str,
        model: str,
        *,
        timeout: float = 120.0,
        temperature: float = 0.7,
        num_predict: int = 512,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout
        self._temperature = temperature
        self._num_predict = num_predict
        # Um client persistente reaproveita conexoes TCP (keep-alive),
        # reduzindo latencia em chamadas sucessivas.
        self._client = httpx.Client(timeout=timeout)

    @property
    def model(self) -> str:
        return self._model

    @property
    def base_url(self) -> str:
        return self._base_url

    def chat(
        self,
        messages: Iterable[ChatMessage],
        *,
        system: str | None = None,
    ) -> str:
        payload_messages: list[dict] = []
        if system:
            payload_messages.append({"role": "system", "content": system})
        payload_messages.extend(dict(m) for m in messages)

        payload = {
            "model": self._model,
            "messages": payload_messages,
            "stream": False,
            "options": {
                "temperature": self._temperature,
                "num_predict": self._num_predict,
            },
        }

        try:
            response = self._client.post(
                f"{self._base_url}/api/chat", json=payload
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise LLMError(
                f"Ollama retornou HTTP {exc.response.status_code}: "
                f"{exc.response.text[:200]}"
            ) from exc
        except httpx.RequestError as exc:
            raise LLMError(f"Falha ao conectar ao Ollama em {self._base_url}: {exc}") from exc

        try:
            data = response.json()
            return data["message"]["content"].strip()
        except (KeyError, ValueError) as exc:
            raise LLMError(f"Resposta inesperada do Ollama: {response.text[:200]}") from exc

    def health(self) -> bool:
        try:
            response = self._client.get(
                f"{self._base_url}/api/tags", timeout=5.0
            )
            return response.status_code == 200
        except httpx.RequestError:
            return False

    def ensure_model(self) -> bool:
        """Verifica se o modelo configurado esta disponivel localmente."""
        try:
            response = self._client.get(
                f"{self._base_url}/api/tags", timeout=10.0
            )
            response.raise_for_status()
            tags = {m.get("name") for m in response.json().get("models", [])}
            # Ollama retorna nomes como "llama3.2:1b"; tambem aceita prefixos.
            return self._model in tags or any(
                name.startswith(self._model.split(":")[0]) for name in tags
            )
        except httpx.RequestError:
            return False

    def close(self) -> None:
        self._client.close()

    def __del__(self) -> None:  # melhor esforco
        try:
            self.close()
        except Exception:
            pass
