"""Carrega as configurações do banco a partir de variáveis de ambiente / .env."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from .errors import ConfigError

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)


@dataclass(frozen=True)
class DBConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    @classmethod
    def from_env(cls) -> "DBConfig":
        try:
            host = os.environ["DB_HOST"]
            user = os.environ["DB_USER"]
            password = os.environ["DB_PASSWORD"]
            database = os.environ["DB_NAME"]
        except KeyError as exc:
            missing = exc.args[0]
            raise ConfigError(
                f"Variável de ambiente obrigatória ausente: {missing}. "
                "Copie .env.example para .env e preencha os valores."
            ) from exc

        port_raw = os.environ.get("DB_PORT", "3306")
        try:
            port = int(port_raw)
        except ValueError as exc:
            raise ConfigError(
                f"DB_PORT deve ser um número inteiro. Valor atual: {port_raw!r}."
            ) from exc

        return cls(host=host, port=port, user=user, password=password, database=database)


_cached: DBConfig | None = None


def get_db_config() -> DBConfig:
    """Carrega a configuração sob demanda (evita falha em import time)."""
    global _cached
    if _cached is None:
        _cached = DBConfig.from_env()
    return _cached
