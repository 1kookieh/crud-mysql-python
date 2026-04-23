"""Exceções de domínio da aplicação."""
from __future__ import annotations


class AppError(Exception):
    """Erro base com mensagem amigável para o usuário."""


class ConfigError(AppError):
    """Falha de configuração (variáveis de ambiente, .env)."""


class ValidationError(AppError):
    """Entrada do usuário inválida."""


class DatabaseError(AppError):
    """Falha de comunicação ou execução no MySQL."""
