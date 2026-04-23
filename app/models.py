"""Modelos de domínio."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Registro:
    id: int
    nome: str
    email: str
    telefone: str | None
    criado_em: datetime | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> "Registro":
        return cls(
            id=int(row["id"]),
            nome=row["nome"],
            email=row["email"],
            telefone=row.get("telefone"),
            criado_em=row.get("criado_em"),
        )
