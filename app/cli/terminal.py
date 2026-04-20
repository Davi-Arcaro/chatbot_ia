"""Interface de linha de comando do Chatbot Eliane.

Uso::

    python main.py

Esta CLI usa o mesmo servico ``Chatbot`` da API. Assim, qualquer mudanca
de comportamento no LLM se reflete nos dois canais sem duplicacao de
logica.
"""

from __future__ import annotations

import sys

from app.core.config import TEMAS, get_settings
from app.llm.base import LLMError
from app.llm.ollama import OllamaClient
from app.services.chatbot import Chatbot


# --- Interface textual ---------------------------------------------------

def exibir_boas_vindas() -> None:
    print("\n" + "=" * 48)
    print("  CHATBOT EDUCACIONAL ELIANE - Bem-vindo!")
    print("=" * 48)


def selecionar_tema() -> str:
    """Mostra os temas e devolve o escolhido pelo usuario."""
    print("\nEscolha um tema:")
    for numero, nome in TEMAS.items():
        print(f"  {numero}. {nome}")
    print(f"  {len(TEMAS) + 1}. Outro (digite o tema desejado)")

    while True:
        escolha = input("\nDigite o numero do tema: ").strip()

        if escolha in TEMAS:
            tema = TEMAS[escolha]
            print(f"\nTema selecionado: {tema}")
            return tema

        if escolha == str(len(TEMAS) + 1):
            tema_custom = input("Digite o tema desejado: ").strip()
            if tema_custom:
                print(f"\nTema selecionado: {tema_custom}")
                return tema_custom
            print("Tema nao pode ser vazio. Tente novamente.")
            continue

        print("Opcao invalida. Tente novamente.")


def exibir_ajuda() -> None:
    print("\n--- Comandos disponiveis ---")
    print("  sair     - Encerra o chatbot")
    print("  quiz     - Ativa o modo quiz")
    print("  conversa - Volta ao modo conversa")
    print("  ajuda    - Exibe esta mensagem")
    print("----------------------------\n")


# --- Quiz ----------------------------------------------------------------

def modo_quiz(bot: Chatbot) -> bool:
    """Roda o loop de quiz ate o usuario voltar para 'conversa' ou sair.

    Retorna ``True`` se o usuario quer continuar no modo conversa,
    ``False`` se digitou 'sair'.
    """
    print("\n--- MODO QUIZ ATIVADO ---")
    print(f"Tema: {bot.tema}")
    print("Digite 'conversa' para voltar ou 'sair' para encerrar.\n")

    acertos = 0
    erros = 0
    total = 0

    while True:
        print("Gerando pergunta...")
        try:
            quiz = bot.gerar_quiz()
        except LLMError as exc:
            print(f"\nErro ao gerar pergunta: {exc}")
            print("Voltando ao modo conversa.\n")
            return True

        if quiz is None:
            print("Nao foi possivel gerar a pergunta. Tentando novamente...\n")
            continue

        total += 1
        print(f"\nPergunta {total}:")
        print(f"  {quiz['pergunta']}\n")
        for letra, texto in quiz["alternativas"].items():
            print(f"  {letra}) {texto}")

        while True:
            resposta_usuario = input("\nSua resposta (A/B/C/D): ").strip().lower()

            if resposta_usuario == "sair":
                _exibir_placar(acertos, erros, total)
                return False

            if resposta_usuario == "conversa":
                _exibir_placar(acertos, erros, total)
                print("\nVoltando ao modo conversa...\n")
                return True

            if resposta_usuario.upper() in ("A", "B", "C", "D"):
                break

            print("Resposta invalida. Digite A, B, C ou D.")

        if resposta_usuario.upper() == quiz["resposta"]:
            acertos += 1
            print("\nCorreto!")
        else:
            erros += 1
            print(f"\nIncorreto. A resposta certa era: {quiz['resposta']}")

        if quiz["explicacao"]:
            print(f"Explicacao: {quiz['explicacao']}")

        print(f"\nPlacar atual: {acertos} acertos | {erros} erros")
        print("-" * 40)


def _exibir_placar(acertos: int, erros: int, total: int) -> None:
    if total > 0:
        print(f"\n{'=' * 30}")
        print("  PLACAR FINAL DO QUIZ")
        print(f"  Acertos: {acertos}/{total}")
        print(f"  Erros:   {erros}/{total}")
        percentual = (acertos / total) * 100
        print(f"  Aproveitamento: {percentual:.0f}%")
        print(f"{'=' * 30}")


# --- Loop principal ------------------------------------------------------

def loop_conversa(bot: Chatbot) -> None:
    print('Digite suas perguntas. Para sair, digite "sair".')
    print('Digite "ajuda" para ver todos os comandos.\n')

    while True:
        print("-" * 48)

        try:
            entrada = input("Voce: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nAte a proxima! Bons estudos!")
            return

        if not entrada:
            print("(Digite uma pergunta ou 'ajuda' para ver os comandos)")
            continue

        comando = entrada.lower()
        if comando == "sair":
            print("\nAte a proxima! Bons estudos!")
            return

        if comando == "ajuda":
            exibir_ajuda()
            continue

        if comando == "quiz":
            continuar = modo_quiz(bot)
            if not continuar:
                print("\nAte a proxima! Bons estudos!")
                return
            continue

        try:
            resposta = bot.enviar_mensagem(entrada)
            print(f"\nProfessor: {resposta}")
        except LLMError as exc:
            print(f"\nDesculpe, ocorreu um erro ao processar sua pergunta: {exc}")
            print("Verifique se o servico Ollama esta rodando e tente novamente.\n")


# --- Entry point ---------------------------------------------------------

def run() -> int:
    """Ponto de entrada da CLI. Retorna um codigo de saida para o shell."""
    settings = get_settings()

    llm = OllamaClient(
        base_url=settings.ollama_url,
        model=settings.ollama_model,
        timeout=settings.ollama_timeout,
        temperature=settings.ollama_temperature,
        num_predict=settings.ollama_num_predict,
    )

    exibir_boas_vindas()

    if not llm.health():
        print(
            f"\nERRO: servico Ollama nao encontrado em {settings.ollama_url}."
            "\nInicie o Ollama (ex.: `ollama serve`) ou suba o docker-compose."
        )
        return 1

    if not llm.ensure_model():
        print(
            f"\nAVISO: modelo '{settings.ollama_model}' nao parece estar baixado."
            f"\nExecute antes: `ollama pull {settings.ollama_model}`"
        )

    tema = selecionar_tema()
    bot = Chatbot(
        tema,
        llm,
        max_history_messages=settings.max_history_messages,
        max_response_words=settings.max_response_words,
    )

    try:
        loop_conversa(bot)
    finally:
        llm.close()
    return 0


if __name__ == "__main__":
    sys.exit(run())
