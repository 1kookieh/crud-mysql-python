"""Operações CRUD sobre a tabela `registros`."""
from __future__ import annotations

import re

from mysql.connector import Error as MySQLError

from .database import get_connection, transaction, wrap_mysql_error
from .errors import ValidationError
from .models import Registro

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _clean(nome: str, email: str, telefone: str | None) -> tuple[str, str, str | None]:
    nome_c = (nome or "").strip()
    email_c = (email or "").strip().lower()
    tel_c = (telefone or "").strip() or None
    if not nome_c:
        raise ValidationError("O campo 'nome' é obrigatório.")
    if len(nome_c) > 100:
        raise ValidationError("O campo 'nome' deve ter até 100 caracteres.")
    if not email_c:
        raise ValidationError("O campo 'email' é obrigatório.")
    if len(email_c) > 120 or not _EMAIL_RE.match(email_c):
        raise ValidationError("Email em formato inválido.")
    if tel_c and len(tel_c) > 30:
        raise ValidationError("O campo 'telefone' deve ter até 30 caracteres.")
    return nome_c, email_c, tel_c


def create_registro(nome: str, email: str, telefone: str | None) -> int:
    nome_c, email_c, tel_c = _clean(nome, email, telefone)
    sql = "INSERT INTO registros (nome, email, telefone) VALUES (%s, %s, %s)"
    try:
        with transaction() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (nome_c, email_c, tel_c))
                return cur.lastrowid
    except MySQLError as exc:
        raise wrap_mysql_error(exc) from exc


def list_registros() -> list[Registro]:
    sql = "SELECT id, nome, email, telefone, criado_em FROM registros ORDER BY id DESC"
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(sql)
                rows = cur.fetchall()
        return [Registro.from_row(r) for r in rows]
    except MySQLError as exc:
        raise wrap_mysql_error(exc) from exc


def update_registro(registro_id: int, nome: str, email: str, telefone: str | None) -> None:
    nome_c, email_c, tel_c = _clean(nome, email, telefone)
    sql = "UPDATE registros SET nome=%s, email=%s, telefone=%s WHERE id=%s"
    try:
        with transaction() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (nome_c, email_c, tel_c, registro_id))
                if cur.rowcount == 0:
                    raise ValidationError("Registro não encontrado para atualização.")
    except MySQLError as exc:
        raise wrap_mysql_error(exc) from exc


def delete_registro(registro_id: int) -> None:
    sql = "DELETE FROM registros WHERE id=%s"
    try:
        with transaction() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (registro_id,))
                if cur.rowcount == 0:
                    raise ValidationError("Registro não encontrado para exclusão.")
    except MySQLError as exc:
        raise wrap_mysql_error(exc) from exc
