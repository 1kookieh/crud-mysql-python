"""Inicializa o banco de dados criando o schema.

Uso:
    py scripts/init_db.py

Conecta-se ao MySQL usando as credenciais do .env (sem selecionar
banco) e executa os statements de sql/schema.sql separadamente
(evitando o modo `multi` deprecado do mysql-connector).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import mysql.connector
from mysql.connector import Error as MySQLError

from app.config import get_db_config


def _split_statements(sql: str) -> list[str]:
    """Divide o SQL em statements, removendo comentários de linha."""
    lines: list[str] = []
    for raw in sql.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("--"):
            continue
        lines.append(raw)
    cleaned = "\n".join(lines)
    statements = [s.strip() for s in re.split(r";\s*(?:\n|$)", cleaned) if s.strip()]
    return statements


def main() -> int:
    schema_path = ROOT / "sql" / "schema.sql"
    if not schema_path.exists():
        print(f"[erro] Arquivo não encontrado: {schema_path}")
        return 1

    try:
        cfg = get_db_config()
    except Exception as exc:
        print(f"[erro] Configuração inválida: {exc}")
        return 1

    try:
        conn = mysql.connector.connect(
            host=cfg.host,
            port=cfg.port,
            user=cfg.user,
            password=cfg.password,
            connection_timeout=5,
        )
    except MySQLError as exc:
        print(f"[erro] Falha ao conectar no MySQL: {exc}")
        return 2

    try:
        sql = schema_path.read_text(encoding="utf-8")
        with conn.cursor() as cur:
            for stmt in _split_statements(sql):
                cur.execute(stmt)
        conn.commit()
    except MySQLError as exc:
        conn.rollback()
        print(f"[erro] Falha ao executar schema.sql: {exc}")
        return 3
    finally:
        conn.close()

    print(f"[ok] Banco '{cfg.database}' inicializado com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
