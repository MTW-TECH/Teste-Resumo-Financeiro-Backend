from sqlalchemy import Boolean, Column, Integer, String

from app.infrastructure.database import RemoteBase


class CompanyModel(RemoteBase):

    __tablename__ = "empresa"
    __table_args__ = {"schema": "candidato_paulo"}

    id = Column("Id", Integer, primary_key=True)
    nome = Column("Nome", String)
    cnpj = Column("Cnpj", String)
    uf = Column("Uf", String)
    cidade = Column("Cidade", String)
    ativo = Column("Ativo", Boolean)
    regime_atual = Column("RegimeAtual", String)
