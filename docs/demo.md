# Demonstração

Este documento descreve como demonstrar o `crud-mysql-python` sem inventar imagens ou resultados.

## Demonstração visual

[PREENCHER: adicionar screenshot real da tela principal em `docs/img/app.png`]

[PREENCHER: opcionalmente adicionar GIF curto em `docs/img/demo.gif` mostrando cadastro, busca, edição e exclusão]

## Fluxo recomendado para apresentação

1. Abrir a aplicação com `py main.py`.
2. Cadastrar um registro fictício.
3. Buscar pelo nome ou e-mail.
4. Editar telefone ou nome.
5. Excluir o registro com confirmação.
6. Mostrar o tratamento de erro com e-mail inválido.

## Dados fictícios para demonstração

Use apenas dados fictícios:

```text
Nome: Maria Teste
Email: maria.teste@example.com
Telefone: (62) 99999-0000
```

## O que destacar em entrevista

- A interface não acessa o banco diretamente.
- A camada `crud.py` concentra validações.
- A camada `database.py` cuida de conexão, transação e tradução de erros.
- Credenciais ficam fora do código por meio de `.env`.
- O projeto representa um sistema interno simples, comum em ambientes administrativos.
