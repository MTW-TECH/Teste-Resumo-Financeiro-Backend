from sqlalchemy import Numeric, Column, String

from app.infrastructure.database import RemoteBase


class LancamentoRateioModel(RemoteBase):
    __tablename__ = "lancamento_rateio"
    __table_args__ = {"schema": "candidato_paulo"}

    id = Column("Id", String, primary_key=True)
    id_lancamento = Column("IdLancamento", String)
    id_categoria = Column("IdCategoria", String)
    valor = Column("Valor", Numeric)
    percentual = Column("Percentual", Numeric)
