"""Templates de prompt usados pelo chatbot educacional.

Mantemos prompts separados da logica para facilitar ajustes sem mexer nos
servicos. Todos os prompts sao em portugues brasileiro, coerentes com o
publico-alvo do chatbot.
"""

from __future__ import annotations


SYSTEM_PROMPT_TEMPLATE = (
    "Voce e um professor especialista em {TEMA}. Seu objetivo e ensinar "
    "conceitos de forma clara, didatica e objetiva. "
    "Responda SEMPRE em portugues brasileiro, usando linguagem simples, "
    "exemplos praticos e analogias quando ajudarem a compreensao. "
    "Limite cada resposta a no maximo {MAX_WORDS} palavras. "
    "Se o aluno perguntar algo fora do tema {TEMA}, informe educadamente "
    "que voce so pode ajudar com assuntos relacionados a {TEMA}."
)


QUIZ_PROMPT_TEMPLATE = (
    "Gere UMA pergunta objetiva de nivel medio sobre {TEMA}. "
    "A pergunta deve ter 4 alternativas (A, B, C, D) com apenas uma correta. "
    "Responda EXATAMENTE no formato abaixo, sem comentarios adicionais:\n"
    "PERGUNTA: <texto da pergunta>\n"
    "A) <alternativa>\n"
    "B) <alternativa>\n"
    "C) <alternativa>\n"
    "D) <alternativa>\n"
    "RESPOSTA: <letra correta em maiusculo>\n"
    "EXPLICACAO: <breve explicacao de por que a resposta esta correta>"
)


def build_system_prompt(tema: str, max_words: int = 150) -> str:
    """Monta o system prompt com o tema e o limite de palavras."""
    return SYSTEM_PROMPT_TEMPLATE.replace("{TEMA}", tema).replace(
        "{MAX_WORDS}", str(max_words)
    )


def build_quiz_prompt(tema: str) -> str:
    """Monta o prompt de quiz com o tema escolhido."""
    return QUIZ_PROMPT_TEMPLATE.replace("{TEMA}", tema)
