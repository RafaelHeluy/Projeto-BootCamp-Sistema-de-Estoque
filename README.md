# Sistema de Estoque

Sistema de gerenciamento de estoque com arquitetura web em Python + JavaScript, persistência em SQLite e interface em HTML/CSS.

## Funcionalidades

- Cadastro de produtos
- Edição e remoção de itens
- Busca por nome e categoria
- Controle de quantidade mínima
- Alertas de estoque baixo
- Entrada e saída de itens do estoque
- Histórico de movimentações
- Resumo financeiro do inventário
- API REST em Python para integração e testes automatizados
- Ambiente Docker para execução simples

## Arquitetura entregue

- Frontend: HTML, CSS e JavaScript
- Backend: Python + Flask
- Persistência: SQLite
- Testes: pytest + pytest-cov
- Execução: servidor Flask em porta 5000

## Requisitos

- Python 3.11+
- pip
- Docker (opcional)

## Execução local

1. Crie o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências

```bash
pip install -r requirements.txt
```

3. Inicie o backend

```bash
python app.py
```

4. Acesse a aplicação

```text
http://localhost:5000
```

## Execução com Docker

```bash
docker compose up --build
```

Depois acesse:

```text
http://localhost:5000
```

## Estrutura de arquivos

- `app.py` — aplicação Flask principal
- `index.html` — interface do usuário
- `style.css` — estilos da interface
- `script.js` — cliente web para consumir a API
- `tests/` — testes automatizados
- `docs/as-built.md` — documentação técnica As-Built
- `docs/test-harness.md` — roteiro de validação
- `docs/demo.md` — material de demonstração

## Observação

Os dados são persistidos em banco SQLite local (`data/stock.db`), permitindo execução simples sem infraestrutura externa.

## Release

A branch de release foi criada em `release/v1.0.0` seguindo a convenção semver para a entrega da versão final.
