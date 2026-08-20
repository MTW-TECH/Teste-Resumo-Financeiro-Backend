from sqlalchemy import Boolean, Column, Date, DateTime, Numeric, String

from app.infrastructure.database import RemoteBase


class LancamentoModel(RemoteBase):
    __tablename__ = "lancamento"
    __table_args__ = {"schema": "candidato_paulo"}

    id = Column("Id", String, primary_key=True)
    data_criacao = Column("DataCriacao", DateTime)
    data_atualizacao = Column("DataAtualizacao", DateTime)
    ativo = Column("Ativo", Boolean)
    excluido = Column("Excluido", Boolean)
    id_usuario = Column("IdUsuario", String)
    data_lancamento = Column("DataLancamento", DateTime)
    data_vencimento = Column("DataVencimento", Date)
    contato = Column("Contato", String)
    id_categoria = Column("IdCategoria", String)
    detalhamento = Column("Detalhamento", String)
    valor = Column("Valor", Numeric)
    tipo_lancamento = Column("TipoLancamento", String)
    id_empresa = Column("IdEmpresa", String)
    chave = Column("Chave", String)
    tipo = Column("Tipo", String)
