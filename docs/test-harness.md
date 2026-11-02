# Test Harness e Cobertura

## Objetivo

Validar a aplicação de estoque em nível de API, incluindo criação, edição, movimentação e reset de dados.

## Comandos de execução

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q --cov=app --cov-report=term-missing --cov-report=html
```

## Escopo validado

- `GET /api/health`
- `POST /api/products`
- `PUT /api/products/:id`
- `DELETE /api/products/:id`
- `POST /api/products/:id/movement`
- `GET /api/movements`
- `GET /api/summary`
- `POST /api/products/reset`

## Critérios de aprovação

- Todos os testes devem retornar status 200/201 esperados.
- Nenhuma falha de execução ou falha conhecida deve permanecer.
- Cobertura de linhas mínima recomendada: 90%+

## Resultado esperado

Ao final da execução, o relatório HTML será gerado em `htmlcov/index.html` e a cobertura será exibida no terminal.
