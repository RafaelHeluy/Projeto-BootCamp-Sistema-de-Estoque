from app import create_app


def test_health_endpoint():
    app = create_app()
    client = app.test_client()
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'


def test_crud_flow_for_products():
    app = create_app()
    client = app.test_client()

    create = client.post('/api/products', json={
        'name': 'Mouse Gamer',
        'category': 'Periféricos',
        'quantity': 12,
        'min_stock': 3,
        'unit_price': 120.50,
        'supplier': 'Tech Supply',
    })
    assert create.status_code == 201
    product = create.get_json()
    product_id = product['id']

    listed = client.get('/api/products')
    assert listed.status_code == 200
    data = listed.get_json()
    assert any(item['id'] == product_id for item in data)

    updated = client.put(f'/api/products/{product_id}', json={
        'name': 'Mouse Gamer Pro',
        'category': 'Periféricos',
        'quantity': 10,
        'min_stock': 2,
        'unit_price': 150.00,
        'supplier': 'Tech Supply',
    })
    assert updated.status_code == 200

    details = client.get('/api/products')
    assert any(item['name'] == 'Mouse Gamer Pro' for item in details.get_json())

    deleted = client.delete(f'/api/products/{product_id}')
    assert deleted.status_code == 200


def test_stock_movements_and_summary():
    app = create_app()
    client = app.test_client()

    product = client.post('/api/products', json={
        'name': 'Teclado',
        'category': 'Periféricos',
        'quantity': 5,
        'min_stock': 2,
        'unit_price': 200.00,
        'supplier': 'Tecnotron',
    }).get_json()
    product_id = product['id']

    entry = client.post(f'/api/products/{product_id}/movement', json={
        'type': 'entry',
        'quantity': 7,
        'notes': 'Reposição de estoque',
    })
    assert entry.status_code == 200

    exit = client.post(f'/api/products/{product_id}/movement', json={
        'type': 'exit',
        'quantity': 3,
        'notes': 'Venda do dia',
    })
    assert exit.status_code == 200

    summary = client.get('/api/summary')
    assert summary.status_code == 200
    summary_payload = summary.get_json()
    assert summary_payload['total_products'] >= 1
    assert summary_payload['total_quantity'] >= 9

    movements = client.get('/api/movements')
    assert movements.status_code == 200
    movement_data = movements.get_json()
    assert len(movement_data) >= 2
    assert any(item['type'] == 'entry' for item in movement_data)
    assert any(item['type'] == 'exit' for item in movement_data)


def test_reset_endpoint():
    app = create_app()
    client = app.test_client()

    client.post('/api/products', json={
        'name': 'Monitor',
        'category': 'Informática',
        'quantity': 4,
        'min_stock': 1,
        'unit_price': 800,
        'supplier': 'CompuMax',
    })

    reset = client.post('/api/products/reset')
    assert reset.status_code == 200

    products = client.get('/api/products')
    assert products.get_json() == []
