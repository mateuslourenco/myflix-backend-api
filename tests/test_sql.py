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


def test_create_serie():
    response = client.post(
        "/series",
        json={"titulo": "Serie 1", "ano": "2022", "genero": "acao", "qtd_temporadas": 3},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["titulo"] == "Serie 1"
    assert data["ano"] == 2022
    assert data["genero"] == "acao"
    assert data["qtd_temporadas"] == 3
    assert "id" in data
    serie_id = data["id"]

    response = client.get(f"/series/{serie_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["titulo"] == "Serie 1"
    assert data["ano"] == 2022
    assert data["genero"] == "acao"
    assert data["qtd_temporadas"] == 3
    assert data["id"] == serie_id
