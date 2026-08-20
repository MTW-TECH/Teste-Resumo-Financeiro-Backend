from sqlalchemy import Boolean, Column, Integer, String

from app.infrastructure.database import RemoteBase


class CompanyModel(RemoteBase):

    __tablename__ = "empresa"
    __table_args__ = {"schema": "candidato_paulo"}

    id = Column("Id", Integer, primary_key=True)
    name = Column("Nome", String)
    cnpj = Column("Cnpj", String)
    state = Column("Uf", String)
    city = Column("Cidade", String)
    active = Column("Ativo", Boolean)
    tax_regime = Column("RegimeAtual", String)
