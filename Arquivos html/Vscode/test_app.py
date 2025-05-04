import pytest
from servidor import app  # Importe sua aplicação Flask

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_salvar_estado_ligada(client):
    response = client.post('/sensor', json={'estado': 'Ligada'})
    assert response.status_code == 200
    assert b"Estado salvo no banco de dados!" in response.data

def test_salvar_estado_desligada(client):
    # Assumindo que já existe um estado "Ligada" no banco para poder desligar
    response = client.post('/sensor', json={'estado': 'Desligada'})
    assert response.status_code == 200
    assert b"Estado salvo no banco de dados!" in response.data

def test_obter_dados(client):
    response = client.get('/dados')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert isinstance(data, list)