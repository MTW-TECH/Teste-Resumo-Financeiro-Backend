from sqlalchemy import Boolean, Column, Date, DateTime, String

from app.infrastructure.database import RemoteBase


class EmpresaFinanceiroModel(RemoteBase):
    __tablename__ = "empresa_financeiro"
    __table_args__ = {"schema": "candidato_paulo"}

    id = Column("Id", String, primary_key=True)
    id_empresa = Column("IdEmpresa", String)
    ativo = Column("Ativo", Boolean)
    inicio_vigencia = Column("InicioVigencia", Date)
    fim_vigencia = Column("FimVigencia", Date)
    data_criacao = Column("DataCriacao", DateTime)
