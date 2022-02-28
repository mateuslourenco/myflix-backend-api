from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from src.schemas.schemas import Serie
from src.infra.sqlalchemy.config.database import get_db, criar_db
from src.infra.sqlalchemy.repositorios.serie import RepositorioSerie

criar_db()

app = FastAPI()


@app.get('/', status_code=status.HTTP_200_OK)
def home():
    return {'Mensagem': 'MyFlix back-end API'}


@app.get('/series', status_code=status.HTTP_200_OK)
def listar_series(db: Session = Depends(get_db)):
    series = RepositorioSerie(db).listar_series()
    return series


@app.post('/series', status_code=status.HTTP_201_CREATED, response_model=Serie)
def criar_serie(serie: Serie, db: Session = Depends(get_db)):
    serie_criada = RepositorioSerie(db).criar(serie)
    return serie_criada


@app.get('/series/{serie_id}')
def listar_serie(serie_id: int, db: Session = Depends(get_db)):
    serie = RepositorioSerie(db).listar_serie(serie_id=serie_id)
    return serie
