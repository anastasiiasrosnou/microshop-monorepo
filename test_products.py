import pytest
from products_service.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client


def test_get_products(client):
    rv = client.get('/products')
    assert rv.status_code == 200
    assert isinstance(rv.json, list)
    assert len(rv.json) > 0
    assert 'name' in rv.json[0]
