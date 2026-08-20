from sqlalchemy import Boolean, Column, String

from app.infrastructure.database import RemoteBase


class CategoriaModel(RemoteBase):
    __tablename__ = "categoria"
    __table_args__ = {"schema": "candidato_paulo"}

    id = Column("Id", String, primary_key=True)
    nome = Column("Nome", String)
    tipo = Column("Tipo", String)
    tipo_lancamento = Column("TipoLancamento", String)
    compoe_custo = Column("CompoeCusto", Boolean)
