"""Camada de conexão reutilizável com o MySQL."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import mysql.connector
from mysql.connector import Error as MySQLError
from mysql.connector.pooling import MySQLConnectionPool

from .config import get_db_config
from .errors import DatabaseError

_POOL: MySQLConnectionPool | None = None

# Mapeamento de códigos comuns do MySQL para mensagens compreensíveis.
_FRIENDLY_MESSAGES: dict[int, str] = {
    1045: "Usuário ou senha do banco inválidos. Verifique o arquivo .env.",
    1049: "Banco de dados não encontrado. Execute o script sql/schema.sql.",
    1062: "Já existe um registro com este valor único (possivelmente email duplicado).",
    1146: "Tabela não encontrada. Execute o script sql/schema.sql.",
    1452: "Violação de chave estrangeira.",
    2003: "Não foi possível conectar ao MySQL. Verifique se o serviço está ativo.",
    2005: "Host do MySQL não encontrado. Verifique DB_HOST no .env.",
    2013: "Conexão com o MySQL perdida durante a operação.",
}


def _get_pool() -> MySQLConnectionPool:
    global _POOL
    if _POOL is None:
        cfg = get_db_config()
        try:
            _POOL = MySQLConnectionPool(
                pool_name="crud_app_pool",
                pool_size=5,
                host=cfg.host,
                port=cfg.port,
                user=cfg.user,
                password=cfg.password,
                database=cfg.database,
                charset="utf8mb4",
                use_pure=True,
                autocommit=False,
                connection_timeout=5,
            )
        except MySQLError as exc:
            raise wrap_mysql_error(exc) from exc
    return _POOL


@contextmanager
def get_connection() -> Iterator[mysql.connector.MySQLConnection]:
    try:
        conn = _get_pool().get_connection()
    except MySQLError as exc:
        raise wrap_mysql_error(exc) from exc
    try:
        yield conn
    finally:
        try:
            conn.close()
        except MySQLError:
            pass


@contextmanager
def transaction() -> Iterator[mysql.connector.MySQLConnection]:
    with get_connection() as conn:
        try:
            yield conn
            conn.commit()
        except Exception:
            try:
                conn.rollback()
            except MySQLError:
                pass
            raise


def wrap_mysql_error(exc: MySQLError) -> DatabaseError:
    code = getattr(exc, "errno", None)
    friendly = _FRIENDLY_MESSAGES.get(code) if code else None
    if friendly:
        return DatabaseError(friendly)
    msg = getattr(exc, "msg", None) or str(exc)
    return DatabaseError(f"Erro no banco de dados: {msg}")
