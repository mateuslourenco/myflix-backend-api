from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from starlette.responses import Response

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
    return RepositorioSerie(db).criar(serie)


@app.get('/series/{serie_id}')
def obter_serie(response: Response, serie_id: int, db: Session = Depends(get_db)):
    serie = RepositorioSerie(db).obter_serie(serie_id=serie_id)
    if serie is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'msg': 'Serie não localizada'}
    return serie


@app.delete('/series/{serie_id}')
def remover_serie(serie_id: int, db: Session = Depends(get_db)):
    RepositorioSerie(db).remover_serie(serie_id=serie_id)
    return {'msg': 'Removido com sucesso'}
