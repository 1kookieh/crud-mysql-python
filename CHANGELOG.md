# Changelog

Todas as mudanças relevantes deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto segue [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

## [1.0.0] - 2026-04-24

### Added

- Aplicação desktop CRUD em Python + Tkinter + MySQL.
- Operações completas: cadastrar, listar, editar e excluir registros
  (nome, email, telefone).
- Pool de conexões com `connection_timeout=5s` e `pool_size=5`.
- Transações com commit/rollback automáticos via context manager.
- Validação de entrada (nome obrigatório, email no formato correto,
  limites de tamanho).
- Busca em tempo real por nome, email ou telefone.
- Ordenação clicando nos cabeçalhos da tabela (com indicadores ▲/▼).
- Barra de status com contagem de registros e feedback de ações.
- Atalhos de teclado: `F5`, `Esc`, `Ctrl+N`, `Enter`, `Delete`.
- Tradução de códigos de erro do MySQL (1045, 1049, 1062, 1146, 2003,
  2005 etc.) para mensagens amigáveis em português.
- Script `scripts/init_db.py` para aplicar o schema sem depender de
  cliente MySQL externo.
- Documentação em pt-BR: README, arquitetura, decisões, roadmap,
  notas para recrutadores.
- Templates de issue (bug, feature) e pull request.
- Workflow de CI no GitHub Actions (lint + smoke test com `py_compile`).
- Licença MIT.

[Unreleased]: https://github.com/1kookieh/crud-mysql-python/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/1kookieh/crud-mysql-python/releases/tag/v1.0.0
