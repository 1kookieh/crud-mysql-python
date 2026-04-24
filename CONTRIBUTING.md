# Contribuindo

Obrigado pelo interesse em contribuir! Este projeto é mantido como peça de
portfólio, mas melhorias, correções e sugestões são bem-vindas.

## Como reportar um bug

1. Verifique se o problema já não foi reportado em
   [Issues](https://github.com/1kookieh/crud-mysql-python/issues).
2. Abra uma nova issue usando o template **Bug report**.
3. Inclua passos para reproduzir, comportamento esperado e o comportamento
   observado. Prints ou logs ajudam bastante.

## Como sugerir uma melhoria

1. Abra uma issue com o template **Feature request**.
2. Descreva o problema que você quer resolver antes de propor a solução.
3. Tudo bem se for só uma ideia — podemos discutir antes de qualquer código.

## Fluxo para pull requests

1. Faça um fork do repositório.
2. Crie uma branch a partir de `main`:
   ```bash
   git checkout -b feat/minha-melhoria
   ```
3. Faça suas alterações.
4. Garanta que os arquivos compilam:
   ```bash
   python -m py_compile main.py app/*.py scripts/*.py
   ```
5. Commit usando [Conventional Commits](https://www.conventionalcommits.org/pt-br/):
   - `feat:` nova funcionalidade
   - `fix:` correção de bug
   - `docs:` somente documentação
   - `refactor:` refatoração sem mudança de comportamento
   - `chore:` manutenção (build, CI, deps)
   - `test:` testes
6. Faça push e abra um PR preenchendo o template.

## Padrões de código

- **Python 3.10+**, com `from __future__ import annotations` no topo.
- **Type hints** em assinaturas públicas.
- **Docstrings curtas** em módulos e funções não triviais.
- **Exceções de domínio** (`AppError` e subclasses) em vez de `Exception`
  genérico na camada de aplicação.
- **Parametrize queries SQL** sempre (`%s`) — nunca concatene strings.
- **Nomes em português** para domínio (`Registro`, `criado_em`); nomes em
  inglês para termos de engenharia (`pool`, `transaction`, `config`).

## Rodando localmente

Veja o [README](README.md) para o passo a passo de setup (venv, `.env`,
`scripts/init_db.py`).

## Código de conduta

Seja respeitoso. Discussões técnicas são ótimas; ataques pessoais não.
