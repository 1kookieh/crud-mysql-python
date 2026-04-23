"""Ponto de entrada da aplicação."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from tkinter import messagebox

# Permite executar `python main.py` de qualquer diretório.
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    try:
        from app.errors import AppError
        from app.ui import CrudApp
    except Exception as exc:  # erro em import (ex.: dependências ausentes)
        messagebox.showerror("Falha ao iniciar", f"Erro no carregamento: {exc}")
        return 1

    try:
        app = CrudApp()
    except AppError as exc:
        messagebox.showerror("Falha ao iniciar", str(exc))
        return 1
    except Exception as exc:
        messagebox.showerror("Falha ao iniciar", f"Erro inesperado: {exc}")
        return 1

    app.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
