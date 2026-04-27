# Notas para Recrutadores

Guia rápido para quem está avaliando este projeto como peça de portfólio.
O objetivo é deixar claro **o que foi construído**, **quais decisões de
engenharia foram tomadas** e **o que este código demonstra**.

## Resumo em 30 segundos

Aplicação desktop de CRUD escrita em **Python + Tkinter + MySQL**, com:

- Arquitetura em camadas (UI / domínio / infra / config).
- Pool de conexões e transações com rollback automático.
- Validação de entrada e tradução de erros do MySQL em mensagens amigáveis.
- Busca em tempo real, ordenação por coluna, atalhos de teclado.
- Documentação em português, CI no GitHub Actions, templates de issue/PR.

## O que este projeto demonstra

- **Organização de código**: separação clara de responsabilidades entre
  apresentação (Tkinter), domínio (CRUD + validação) e infraestrutura (pool,
  transações).
- **Cuidado com robustez**: `try/except` em todos os pontos de I/O, rollback
  automático em transação, timeout de conexão para não travar a UI.
- **Segurança básica**: queries parametrizadas (sem SQL Injection), `.env`
  fora do repositório, normalização de email + `UNIQUE` no banco.
- **Experiência do usuário**: status bar, atalhos (F5, Esc, Ctrl+N, Enter,
  Delete), preservação de seleção após refresh, mensagens de erro legíveis.
- **Boas práticas de repositório**: Conventional Commits, CHANGELOG, templates
  de issue/PR, workflow de CI, `.gitignore` e `.gitattributes` configurados.

## Onde olhar primeiro

| Arquivo | Por quê |
| --- | --- |
| `app/database.py` | Pool, transações, tradução de `errno` do MySQL. |
| `app/crud.py` | Validação + operações de domínio com transações. |
| `app/ui.py` | Tkinter idiomático, cache em memória, ordenação/filtro. |
| `docs/architecture.md` | Visão macro das camadas. |
| `docs/decisions.md` | ADRs resumidos explicando cada escolha. |

## Executando localmente

Veja o [README](../README.md) — instalação em ~5 comandos, incluindo script
Python (`scripts/init_db.py`) que aplica o schema sem depender de cliente
MySQL externo.

## Stack e versões

- Python 3.10+
- MySQL 8.x
- `mysql-connector-python==9.1.0`
- `python-dotenv==1.0.1`

## Autor

**Igor** — [@1kookieh](https://github.com/1kookieh)
