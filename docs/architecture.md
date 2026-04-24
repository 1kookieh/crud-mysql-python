# Arquitetura

Este documento descreve como a aplicação está organizada e como os módulos se
comunicam. O objetivo é manter responsabilidades bem separadas, facilitando
testes, manutenção e evolução.

## Visão geral em camadas

```
┌────────────────────────┐
│        main.py         │  ponto de entrada / bootstrap
└───────────┬────────────┘
            │
┌───────────▼────────────┐
│        app/ui.py       │  camada de apresentação (Tkinter)
└───────────┬────────────┘
            │
┌───────────▼────────────┐
│       app/crud.py      │  regras de validação + operações de domínio
└───────────┬────────────┘
            │
┌───────────▼────────────┐
│     app/database.py    │  pool de conexões, transações, tradução de erros
└───────────┬────────────┘
            │
┌───────────▼────────────┐
│      app/config.py     │  leitura de .env / DBConfig
└────────────────────────┘
```

Módulos de apoio:

- `app/errors.py` — hierarquia de exceções de domínio (`AppError`,
  `ConfigError`, `ValidationError`, `DatabaseError`).
- `app/models.py` — `dataclass Registro` mais `from_row()` para hidratar
  resultados do cursor `dictionary=True`.

## Princípios

- **UI não conhece SQL**: `ui.py` depende apenas de `crud.py` e das exceções.
- **CRUD não conhece Tkinter**: `crud.py` retorna dados e lança exceções; quem
  decide como exibir é a UI.
- **Erros de infraestrutura viram mensagens amigáveis**: `database.py` mantém
  um mapa de `errno` do MySQL para mensagens em português (1045, 1049, 1062,
  1146, 2003, 2005 etc.).
- **Configuração preguiçosa** (lazy): `config.get_db_config()` só lê variáveis
  de ambiente quando chamado, permitindo que `main.py` capture erros de
  inicialização e exiba um `messagebox`.

## Pool de conexões

`database._get_pool()` cria um único `MySQLConnectionPool` com:

- `pool_size=5` — suficiente para um desktop monousuário.
- `connection_timeout=5` — evita travar a UI em caso de servidor indisponível.
- `use_pure=True` — driver puro em Python (sem binário nativo), mais portável.
- `autocommit=False` — forçamos transações explícitas.
- `charset="utf8mb4"` — suporte pleno a UTF-8 (emojis, acentos).

Conexões são devolvidas ao pool no `finally` de `get_connection()`.

## Transações

O context manager `transaction()`:

1. Pega uma conexão do pool.
2. Dá `yield` para o bloco `with`.
3. Comita ao final se não houver exceção.
4. Em caso de exceção, faz `rollback()` e propaga.

Todas as escritas (`create_registro`, `update_registro`, `delete_registro`) usam
`transaction()`. Leituras usam apenas `get_connection()`.

## Tratamento de erros

- `ValidationError` → `messagebox.showwarning` (entrada do usuário).
- `DatabaseError` → `messagebox.showerror` (infra).
- `AppError` genérico → `messagebox.showerror`.

`wrap_mysql_error()` converte `mysql.connector.Error` em `DatabaseError` com
mensagem traduzida quando o `errno` é conhecido.

## Segurança

- **SQL Injection**: todas as queries usam placeholders `%s`.
- **Credenciais**: lidas de `.env` (ignorado pelo Git).
- **Integridade**: `UNIQUE` em `email`; `NOT NULL` em `nome`/`email`.

## Renderização e UX

- A tabela (`ttk.Treeview`) é re-renderizada a partir de um cache em memória
  (`_all_records` + `_records_by_id`), o que preserva tipos originais (zeros à
  esquerda em telefone, `None` vs string vazia).
- Filtro e ordenação acontecem **em memória** — adequado para o volume típico
  de um CRUD local. Para bases grandes, ver `docs/roadmap.md` (paginação
  server-side).
