# Decisões Técnicas (ADRs resumidos)

Registro das principais escolhas de projeto, suas motivações e alternativas
consideradas.

---

## 1. Tkinter como framework de UI

**Decisão**: usar `tkinter` / `ttk` da biblioteca padrão.

**Motivo**:

- Zero dependências extras para a camada de apresentação.
- Suficiente para um CRUD simples com tabela, formulário e busca.
- Multiplataforma (Windows, Linux, macOS) sem empacotamento adicional.

**Alternativas consideradas**: PyQt/PySide (mais poderoso, mas pesado e com
questões de licença), Kivy (foco em mobile), Flet (requer bundle web).

---

## 2. `mysql-connector-python` em modo `use_pure=True`

**Decisão**: driver oficial da Oracle, em Python puro.

**Motivo**:

- Driver oficial → bom suporte a `errno` e mensagens.
- `use_pure=True` evita dependência de wheel binário, simplificando setup em
  máquinas sem compilador C.
- Pool de conexões nativo (`MySQLConnectionPool`).

**Alternativas**: `PyMySQL` (menos metadados de erro), `SQLAlchemy` (over-
engineering para o escopo atual).

---

## 3. Sem ORM

**Decisão**: escrever SQL à mão com placeholders `%s`.

**Motivo**:

- Escopo pequeno (uma tabela), ORM adicionaria complexidade desnecessária.
- SQL explícito é didático e facilita auditoria de segurança.
- Parametrização nativa do driver já previne SQL Injection.

---

## 4. Pool de conexões mesmo em desktop monousuário

**Decisão**: usar `MySQLConnectionPool` com `pool_size=5`.

**Motivo**:

- Evita custo de handshake a cada operação.
- Simplifica `close()` (o `finally` devolve a conexão em vez de encerrar).
- Prepara o código para eventual refactor para modo servidor / multi-thread.

---

## 5. Transações explícitas com context manager

**Decisão**: `autocommit=False` + `with transaction() as conn:` em toda escrita.

**Motivo**:

- Garante atomicidade mesmo em operações simples (permite evoluir para
  operações multi-tabela).
- O context manager centraliza `commit`/`rollback`, evitando esquecimento.

---

## 6. Exceções de domínio + tradução de `errno`

**Decisão**: hierarquia `AppError → (ConfigError, ValidationError,
DatabaseError)` e mapa de `errno` do MySQL em `_FRIENDLY_MESSAGES`.

**Motivo**:

- A UI só precisa distinguir 3 categorias para escolher `messagebox`.
- O usuário final vê "Usuário ou senha inválidos" em vez de `1045 (28000): ...`.
- Logs preservam a exceção original via `raise ... from exc`.

---

## 7. Carregamento preguiçoso de `.env`

**Decisão**: `get_db_config()` lê variáveis sob demanda; `main.py` captura
`AppError` e exibe `messagebox`.

**Motivo**:

- Falha de configuração é um erro esperado — não deve derrubar o processo com
  stack trace no console.
- Permite iniciar a aplicação e mostrar mensagem gráfica mesmo sem `.env`.

---

## 8. Filtro e ordenação em memória

**Decisão**: manter `_all_records` na UI e filtrar/ordenar em Python.

**Motivo**:

- Volume esperado é baixo (< 10k linhas).
- Resposta imediata ao digitar na busca (`trace_add("write", ...)`).
- Evita ida ao banco a cada tecla.

**Quando revisar**: ver `docs/roadmap.md` — paginação server-side.

---

## 9. Email normalizado para lowercase

**Decisão**: `_clean()` força `.lower()` antes de gravar; `UNIQUE` no banco.

**Motivo**: impede duplicatas como `Joao@x.com` e `joao@x.com`.

---

## 10. Layout do `pack()` com status bar primeiro

**Decisão**: montar a status bar antes da tabela.

**Motivo**: no Tkinter, `pack(side="bottom")` reserva espaço na ordem das
chamadas — montar a status bar antes garante que ela fique sempre visível,
mesmo com janela pequena.
