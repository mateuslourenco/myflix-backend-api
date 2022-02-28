import pytest
from starlette.testclient import TestClient

from src.server import app

client = TestClient(app)


@pytest.fixture
def resp():
    return client.get('/')


def test_status_code(resp):
    assert resp.status_code == 200
    assert resp.json() == {'Mensagem': 'MyFlix back-end API'}