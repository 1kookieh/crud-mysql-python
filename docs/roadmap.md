# Roadmap

Lista viva de melhorias planejadas. Nenhuma delas é bloqueante para o uso atual
— o objetivo é dar visibilidade sobre a direção do projeto.

## Curto prazo

- [ ] **Testes automatizados com `pytest`**
  - Testes unitários para `crud._clean()` (validações).
  - Testes de integração usando um MySQL em container (docker-compose).
- [ ] **Logger rotativo**
  - `logging.handlers.RotatingFileHandler` em `logs/crud_app.log`.
  - Nível configurável via `.env` (`LOG_LEVEL=INFO`).
- [ ] **Screenshot no README**
  - Adicionar `docs/img/app.png` e referência no README.

## Médio prazo

- [ ] **Exportação CSV / Excel**
  - Botão "Exportar" que gera CSV (stdlib) ou XLSX (`openpyxl`).
  - Respeitar o filtro atual da tabela.
- [ ] **Paginação server-side**
  - `LIMIT` + `OFFSET` no `list_registros()`.
  - Controles de "Próxima / Anterior" na UI.
  - Habilitar quando o volume passar de ~10k linhas.
- [ ] **Soft delete**
  - Coluna `deletado_em DATETIME NULL`.
  - `list_registros()` filtra por `deletado_em IS NULL`.
  - Tela opcional de "lixeira" com restauração.
- [ ] **Internacionalização básica**
  - Separar strings em um `messages.py` para permitir traduções futuras.

## Longo prazo

- [ ] **Empacotamento com PyInstaller**
  - Executável `.exe` standalone para Windows.
  - Workflow de release no GitHub Actions (Windows runner).
- [ ] **Migração para SQLAlchemy Core**
  - Ganhar portabilidade (SQLite, PostgreSQL) sem adotar ORM completo.
- [ ] **Modo multiusuário (cliente-servidor)**
  - Separar UI de uma API HTTP/gRPC.
  - Autenticação básica.

## Ideias em avaliação

- Auditoria (tabela `registros_audit` com gatilhos).
- Importação em massa a partir de CSV.
- Tema escuro na UI (`ttk.Style`).
