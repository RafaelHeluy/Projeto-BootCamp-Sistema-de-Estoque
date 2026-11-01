# Sistema de Estoque

Sistema de gerenciamento de estoque em HTML, CSS e JavaScript, com persistência em `localStorage`.

## Funcionalidades

- Cadastro de produtos
- Edição e remoção de itens
- Busca por nome e categoria
- Controle de quantidade mínima
- Alertas de estoque baixo
- Entrada e saída de itens do estoque
- Histórico de movimentações
- Resumo financeiro do inventário

## Como executar

1. Abra o arquivo `index.html` no navegador.
2. Ou utilize um servidor estático simples, por exemplo:

```bash
python -m http.server 8000
```

Depois acesse:

```text
http://localhost:8000
```

## Estrutura

- `index.html` — interface principal
- `style.css` — estilos da aplicação
- `script.js` — lógica do sistema

## Observação

Os dados ficam salvos no navegador via `localStorage`, então o sistema é funcional sem banco de dados.
