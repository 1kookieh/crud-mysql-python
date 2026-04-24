# CRUD Desktop — Python + Tkinter + MySQL

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/1kookieh/crud-mysql-python/actions/workflows/ci.yml/badge.svg)](https://github.com/1kookieh/crud-mysql-python/actions/workflows/ci.yml)

Aplicação desktop para gestão local de registros (nome, email, telefone),
com interface gráfica em Tkinter e persistência em MySQL 8.

> Projeto de portfólio com foco em arquitetura em camadas, pool de conexões,
> transações com rollback automático e tradução de erros do MySQL em mensagens
> amigáveis para o usuário final.

## 🖼️ Demo

> _Screenshot em breve — adicione `docs/img/app.png` e referencie aqui._

---

## ✨ Recursos

- **CRUD completo**: cadastrar, listar, editar e excluir.
- **Busca em tempo real** por nome, email ou telefone.
- **Ordenação** clicando nos cabeçalhos da tabela.
- **Barra de status** com contagem de registros e feedback de ações.
- **Atalhos de teclado** (F5, Esc, Ctrl+N, Enter, Delete).
- **Pool de conexões** com timeout e **transações** em todas as escritas.
- **Mensagens de erro amigáveis** (códigos MySQL traduzidos).
- **Validação** de entrada (nome, email, tamanho máximo).
- **Separação em camadas**: UI / CRUD / database / config / models / errors.

---

## 📁 Estrutura

```
crud_app/
├── main.py                 # ponto de entrada
├── requirements.txt        # dependências
├── .env.example            # modelo de variáveis de ambiente
├── .gitignore
├── LICENSE
├── README.md
├── sql/
│   └── schema.sql          # cria banco e tabela
├── scripts/
│   └── init_db.py          # aplica o schema via Python
└── app/
    ├── __init__.py
    ├── config.py           # carrega .env (lazy)
    ├── database.py         # pool, transações, tradução de erros
    ├── errors.py           # AppError / ValidationError / DatabaseError
    ├── models.py           # dataclass Registro
    ├── crud.py             # CRUD + validações
    └── ui.py               # janela Tkinter
```

---

## ✅ Pré-requisitos

- **Python 3.10+**
- **MySQL 8.x** rodando em `localhost:3306` (ou host/porta equivalentes)

---

## 🚀 Instalação

```powershell
# 1. Clonar o repositório
git clone <url-do-repo>
cd crud_app

# 2. Criar e ativar ambiente virtual
py -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate    # Linux/macOS

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Criar o arquivo .env a partir do modelo
copy .env.example .env        # Windows
# cp .env.example .env        # Linux/macOS
```

Edite o `.env` e preencha as credenciais do seu MySQL:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_NAME=crud_app
```

---

## 🗄️ Criar o banco de dados

**Opção A — via Python (recomendado)**:

```powershell
py scripts/init_db.py
```

**Opção B — via cliente MySQL (Workbench, DBeaver, CLI)**: execute `sql/schema.sql`.

---

## ▶️ Executar

```powershell
py main.py
```

---

## ⌨️ Atalhos

| Atalho | Ação |
| --- | --- |
| `F5` | Recarregar lista |
| `Esc` | Limpar formulário |
| `Ctrl+N` | Novo registro (limpa e foca em Nome) |
| `Enter` (no formulário) | Cadastrar (sem seleção) ou Atualizar (com seleção) |
| `Delete` (fora de campos) | Excluir registro selecionado |

---

## 🧪 Testes manuais

### Inicialização
- [ ] Sem `.env` → mensagem "Variável de ambiente obrigatória ausente".
- [ ] `DB_PORT` inválido → mensagem "DB_PORT deve ser um número inteiro".
- [ ] MySQL parado → mensagem "Não foi possível conectar ao MySQL".

### Create
- [ ] Nome vazio → aviso de validação.
- [ ] Email inválido (`x@y`) → aviso de validação.
- [ ] Email duplicado → "Já existe um registro com este valor único...".
- [ ] Dados válidos → confirmação na barra de status; registro aparece.

### Read / Filtro / Ordenação
- [ ] Digitar na busca → linhas filtram em tempo real.
- [ ] Clicar em cabeçalho → alterna ordenação asc/desc com ▲/▼.
- [ ] Barra de status mostra "X de Y" quando há filtro.

### Update
- [ ] Clicar em linha → formulário preenche (preservando zeros do telefone).
- [ ] Editar e clicar "Atualizar" → seleção mantida após refresh.
- [ ] Atualizar sem seleção → aviso.

### Delete
- [ ] "Excluir" abre diálogo de confirmação.
- [ ] Confirmar → registro some; status atualiza.
- [ ] Cancelar → nada acontece.

---

## 🔐 Segurança

- Todas as queries usam parâmetros (`%s`) → **sem SQL Injection**.
- Escritas executam dentro de **transação** com commit/rollback automáticos.
- Pool de conexões com `connection_timeout=5s`.
- Credenciais ficam em `.env` (ignorado pelo Git).
- Email armazenado em *lowercase* e restrição `UNIQUE` no banco.

---

## 🧱 Schema

```sql
CREATE TABLE registros (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    nome       VARCHAR(100) NOT NULL,
    email      VARCHAR(120) NOT NULL UNIQUE,
    telefone   VARCHAR(30)  NULL,
    criado_em  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🏗️ Arquitetura

```
┌──────────────┐
│    main.py   │  ← ponto de entrada
└──────┬───────┘
       │
┌──────▼───────┐      ┌─────────────┐
│    app/ui    │─────▶│  app/errors │
└──────┬───────┘      └─────────────┘
       │
┌──────▼───────┐      ┌─────────────┐
│   app/crud   │─────▶│ app/models  │
└──────┬───────┘      └─────────────┘
       │
┌──────▼─────────┐    ┌─────────────┐
│  app/database  │───▶│  app/config │──▶ .env
└────────────────┘    └─────────────┘
```

- **ui.py** não acessa banco diretamente.
- **crud.py** valida input e fala com `database.py`.
- **database.py** oferece `get_connection()` e `transaction()` via context managers.
- **config.py** carrega `.env` de forma *lazy* para permitir tratamento de erro.

---

## 🛠️ Solução de problemas

| Sintoma | Causa | Solução |
| --- | --- | --- |
| "Variável de ambiente obrigatória ausente" | `.env` não criado | `copy .env.example .env` e preencha |
| "DB_PORT deve ser um número inteiro" | Valor inválido no `.env` | Ajuste `DB_PORT=3306` |
| "Não foi possível conectar ao MySQL" | Serviço desligado | Inicie o serviço (`net start MySQL80`) |
| "Usuário ou senha do banco inválidos" | Credenciais no `.env` erradas | Revise `DB_USER`/`DB_PASSWORD` |
| "Tabela não encontrada" | Schema não aplicado | `py scripts/init_db.py` |
| "Email em formato inválido" | Entrada malformada | Use `nome@dominio.ext` |

---

## 📦 Dependências

```text
mysql-connector-python==9.1.0
python-dotenv==1.0.1
```

Instaladas com `pip install -r requirements.txt`.

---

## 🗺️ Próximas melhorias

- [ ] Testes automatizados com `pytest`.
- [ ] Paginação server-side.
- [ ] Exportar para CSV/Excel.
- [ ] Empacotamento com PyInstaller.
- [ ] Soft delete.
- [ ] Logger rotativo em `logs/`.

---

## 📄 Licença

MIT — veja [LICENSE](LICENSE).
