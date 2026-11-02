# Especificação Técnica Final (As-Built)

## 1. Visão geral

O sistema implementado é uma aplicação web de gestão de estoque composta por um frontend em HTML/CSS/JavaScript e um backend em Python com Flask. A persistência é realizada em SQLite local, permitindo operação simples e sem dependência de banco externo.

## 2. Arquitetura

### 2.1 Frontend
- Arquivos: `index.html`, `style.css`, `script.js`
- Responsabilidade: renderizar dashboard, formulário de cadastro, listagem de produtos e histórico de movimentações
- Comunicação: consumo de endpoints REST via `fetch()`

### 2.2 Backend
- Arquivo: `app.py`
- Framework: Flask
- Porta: `5000`
- Endpoints principais:
  - `GET /api/health`
  - `GET /api/products`
  - `POST /api/products`
  - `PUT /api/products/<id>`
  - `DELETE /api/products/<id>`
  - `POST /api/products/<id>/movement`
  - `GET /api/movements`
  - `GET /api/summary`
  - `POST /api/products/reset`

### 2.3 Persistência
- Banco: SQLite
- Arquivo: `data/stock.db`
- Tabelas:
  - `products`
  - `movements`

## 3. Estrutura de dados

### 3.1 Produto
- `id`: inteiro
- `name`: texto
- `category`: texto
- `quantity`: inteiro
- `min_stock`: inteiro
- `unit_price`: decimal
- `supplier`: texto
- `created_at`: timestamp
- `updated_at`: timestamp

### 3.2 Movimentação
- `id`: inteiro
- `product_id`: inteiro
- `type`: `entry` ou `exit`
- `quantity`: inteiro
- `notes`: texto opcional
- `created_at`: timestamp

## 4. Regras de negócio

- Produtos devem possuir nome, categoria e fornecedor válidos.
- Quantidade e estoque mínimo são inteiros com valor mínimo de 0.
- Movimentações de saída não podem gerar quantidade negativa.
- O resumo do inventário calcula:
  - total de produtos
  - quantidade total em estoque
  - produtos em nível crítico (`quantity <= min_stock`)
  - valor total do inventário

## 5. Contratos de API

### 5.1 POST /api/products
Request body:
```json
{
  "name": "Teclado",
  "category": "Periféricos",
  "quantity": 12,
  "min_stock": 3,
  "unit_price": 250.0,
  "supplier": "Tech Supply"
}
```

Response:
```json
{
  "id": 1,
  "message": "Produto criado com sucesso"
}
```

### 5.2 PUT /api/products/:id
Atualiza os campos do produto.

### 5.3 POST /api/products/:id/movement
Request body:
```json
{
  "type": "entry",
  "quantity": 5,
  "notes": "Reposição de janeiro"
}
```

### 5.4 GET /api/summary
Response:
```json
{
  "total_products": 10,
  "total_quantity": 150,
  "low_stock": 2,
  "total_value": 45670.5
}
```

## 6. Execução

### 6.1 Local
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### 6.2 Docker
```bash
docker compose up --build
```

## 7. Observações finais

A aplicação entregue representa a versão final do sistema de estoque com backend Python em paralelo ao frontend original, validando operações de cadastro, movimentação e dashboard em uma arquitetura completa, simples e testável.
