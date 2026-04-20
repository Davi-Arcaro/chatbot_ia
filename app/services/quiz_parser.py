"""Parser do texto de quiz retornado pelo LLM.

O modelo local e instruido a responder em um formato estrito (PERGUNTA /
A-D / RESPOSTA / EXPLICACAO). Este modulo converte o texto bruto em dict
estruturado. Retorna ``None`` quando o texto nao segue o formato, para que
a camada superior possa decidir entre tentar novamente ou reportar erro.
"""

from __future__ import annotations

import re
from typing import Optional, TypedDict


class Quiz(TypedDict):
    pergunta: str
    alternativas: dict[str, str]
    resposta: str
    explicacao: str


def parse_quiz(texto: str) -> Optional[Quiz]:
    """Converte o texto bruto do modelo em um dicionario de quiz."""
    if not texto:
        return None

    pergunta_match = re.search(r"PERGUNTA:\s*(.+?)(?=\nA\))", texto, re.DOTALL | re.IGNORECASE)
    alt_a = re.search(r"A\)\s*(.+?)(?=\nB\))", texto, re.DOTALL)
    alt_b = re.search(r"B\)\s*(.+?)(?=\nC\))", texto, re.DOTALL)
    alt_c = re.search(r"C\)\s*(.+?)(?=\nD\))", texto, re.DOTALL)
    alt_d = re.search(r"D\)\s*(.+?)(?=\nRESPOSTA:)", texto, re.DOTALL | re.IGNORECASE)
    resposta_match = re.search(r"RESPOSTA:\s*([A-Da-d])", texto)
    explicacao_match = re.search(r"EXPLICACAO:\s*(.+)", texto, re.DOTALL | re.IGNORECASE)

    if not all([pergunta_match, alt_a, alt_b, alt_c, alt_d, resposta_match]):
        return None

    return Quiz(
        pergunta=pergunta_match.group(1).strip(),
        alternativas={
            "A": alt_a.group(1).strip(),
            "B": alt_b.group(1).strip(),
            "C": alt_c.group(1).strip(),
            "D": alt_d.group(1).strip(),
        },
        resposta=resposta_match.group(1).strip().upper(),
        explicacao=explicacao_match.group(1).strip() if explicacao_match else "",
    )
