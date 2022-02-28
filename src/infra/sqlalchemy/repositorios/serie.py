from sqlalchemy.orm import Session

from src.infra.sqlalchemy.models import models
from src.schemas import schemas


class RepositorioSerie:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, serie: schemas.Serie):
        db_serie = models.Serie(titulo=serie.titulo,
                                ano=serie.ano,
                                genero=serie.genero,
                                qtd_temporadas=serie.qtd_temporadas
                                )
        self.db.add(db_serie)
        self.db.commit()
        self.db.refresh(db_serie)
        return db_serie

    def listar_series(self):
        series = self.db.query(models.Serie).all()
        return series

    def listar_serie(self, serie_id: int):
        return self.db.query(models.Serie).filter(models.Serie.id == serie_id).first()
