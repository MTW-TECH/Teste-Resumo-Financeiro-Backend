from collections import defaultdict

from sqlalchemy import select

from app.domain.entities.financial_summary import FinancialSummary
from app.domain.repositories.financial_repository import FinancialRepository
from app.infrastructure.models.lancamento_model import LancamentoModel


class SqlAlchemyFinancialRepository(FinancialRepository):
    """Reads financial data from candidato_paulo.lancamento in financial_remote."""

    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def get_summary(self) -> FinancialSummary:
        with self._session_factory() as session:
            lancamentos = session.scalars(select(LancamentoModel)).all()

        receita_total = 0.0
        custo_total = 0.0
        taxa_total = 0.0
        monthly = defaultdict(lambda: {"receita": 0.0, "taxa": 0.0})

        for item in lancamentos:
            valor = float(item.valor or 0)
            data = item.data_lancamento or item.data_criacao
            mes = data.strftime("%Y-%m") if data else "sem-data"
            categoria = f"{item.tipo_lancamento or ''} {item.tipo or ''}".lower()

            if "receita" in categoria or "credito" in categoria:
                receita_total += valor
                monthly[mes]["receita"] += valor
            elif "tax" in categoria or "imposto" in categoria:
                taxa_total += valor
                monthly[mes]["taxa"] += valor
            else:
                custo_total += valor

        lucro_total = receita_total - custo_total - taxa_total
        montly_data = [
            {
                "mes": mes,
                "receita": int(values["receita"]),
                "taxa": int(values["taxa"]),
            }
            for mes, values in sorted(monthly.items())
        ]

        return FinancialSummary(
            receita=f"{receita_total:.2f}",
            custos=f"{custo_total:.2f}",
            taxas=f"{taxa_total:.2f}",
            lucro=f"{lucro_total:.2f}",
            lajida=f"{lucro_total:.2f}",
            montlyData=montly_data,
        )
