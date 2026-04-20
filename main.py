"""Entry point do Chatbot Eliane no terminal.

Mantido na raiz por conveniencia (``python main.py``). A logica real esta
em ``app/cli/terminal.py``.
"""

from __future__ import annotations

import sys

from app.cli.terminal import run


if __name__ == "__main__":
    sys.exit(run())
