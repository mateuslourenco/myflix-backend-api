import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.infra.sqlalchemy.config.database import Base, get_db
from src.server import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def resp_post():
    response = client.post(
        "/series",
        json={"titulo": "Serie 1", "ano": "2022", "genero": "acao", "qtd_temporadas": 3},
    )
    return response


@pytest.fixture
def resp_get():
    response = client.get('/series')
    return response


@pytest.fixture
def resp_delete():
    response = client.delete('/series/1')
    return response


def test_criar_serie(resp_post):

    assert resp_post.status_code == 201, resp_post.text
    data = resp_post.json()
    assert data["titulo"] == "Serie 1"
    assert data["ano"] == 2022
    assert data["genero"] == "acao"
    assert data["qtd_temporadas"] == 3
    assert "id" in data
    serie_id = data["id"]

    # Teste obter_serie
    response = client.get(f"/series/{serie_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["Serie"]["titulo"] == "Serie 1"
    assert data["Serie"]["ano"] == 2022
    assert data["Serie"]["genero"] == "acao"
    assert data["Serie"]["qtd_temporadas"] == 3
    assert data["Serie"]["id"] == serie_id


def test_listar_serie(resp_get):
    assert resp_get.status_code == 200
    data = resp_get.json()
    for serie in data:
        assert serie['id']


def test_deletar_serie(resp_delete):
    assert resp_delete.status_code == 200
    data = resp_delete.json()
    assert data == {'msg': 'Removido com sucesso'}

    # Teste obter_serie
    response = client.get(f"/series/{1}")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data == {'msg': 'Serie não localizada'}
