import sys
sys.path.append('..')
from api import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_hello():
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello from FastAPI'}
