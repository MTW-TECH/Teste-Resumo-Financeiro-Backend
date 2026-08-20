from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.sql import text

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
            categorias = session.execute(text("SELECT * FROM candidato_paulo.categoria")).mappings().all()
            rateios = session.execute(text("SELECT * FROM candidato_paulo.lancamento_rateio")).mappings().all()

        totals = {"receita": 0.0, "custos": 0.0, "taxas": 0.0}
        monthly = defaultdict(lambda: {"receita": 0.0, "custos": 0.0, "taxa": 0.0})

        categorias_por_id = self._build_categorias_por_id(categorias)
        rateios_por_lancamento = self._build_rateios_por_lancamento(rateios)

        for item in lancamentos:
            valor = float(item.valor or 0)
            data = item.data_lancamento or item.data_criacao
            mes = data.strftime("%Y-%m") if data else "sem-data"
            classificacao_padrao = f"{item.tipo_lancamento or ''} {item.tipo or ''}".lower()

            rateios_lancamento = rateios_por_lancamento.get(str(item.id), [])
            if not rateios_lancamento:
                self._accumulate_without_rateio(
                    totals=totals,
                    monthly=monthly,
                    mes=mes,
                    valor=valor,
                    classificacao=classificacao_padrao,
                )
                continue

            self._accumulate_with_rateios(
                totals=totals,
                monthly=monthly,
                mes=mes,
                valor_total=valor,
                classificacao_padrao=classificacao_padrao,
                rateios_lancamento=rateios_lancamento,
                categorias_por_id=categorias_por_id,
            )

        lucro_liquido_total = totals["receita"] - totals["custos"] - totals["taxas"]
        ebitda_total = totals["receita"] - totals["custos"]
        montly_data = [
            {
                "mes": mes,
                "receita": int(values["receita"]),
                "custos": int(values["custos"]),
                "taxa": int(values["taxa"]),
            }
            for mes, values in sorted(monthly.items())
        ]

        return FinancialSummary(
            receita=f"{totals['receita']:.2f}",
            custos=f"{totals['custos']:.2f}",
            taxas=f"{totals['taxas']:.2f}",
            lucro_liquido=f"{lucro_liquido_total:.2f}",
            ebitda=f"{ebitda_total:.2f}",
            lucro=f"{lucro_liquido_total:.2f}",
            lajida=f"{ebitda_total:.2f}",
            montlyData=montly_data,
        )

    def _build_categorias_por_id(self, categorias):
        categorias_por_id = {}
        for categoria in categorias:
            categoria_id = self._pick(categoria, "id", "Id")
            if categoria_id:
                categorias_por_id[str(categoria_id)] = categoria
        return categorias_por_id

    def _build_rateios_por_lancamento(self, rateios):
        rateios_por_lancamento = defaultdict(list)
        for rateio in rateios:
            lancamento_id = self._pick(
                rateio,
                "id_lancamento",
                "idlancamento",
                "IdLancamento",
                "lancamento_id",
            )
            if lancamento_id:
                rateios_por_lancamento[str(lancamento_id)].append(rateio)
        return rateios_por_lancamento

    def _accumulate_without_rateio(self, totals, monthly, mes: str, valor: float, classificacao: str):
        receita, custo, taxa = self._classify_amount(
            valor=valor,
            classificacao=classificacao,
            compoe_custo=None,
        )
        self._apply_amounts(totals, monthly, mes, receita, custo, taxa)

    def _accumulate_with_rateios(
        self,
        totals,
        monthly,
        mes: str,
        valor_total: float,
        classificacao_padrao: str,
        rateios_lancamento,
        categorias_por_id,
    ):
        valor_rateios = [
            float(self._pick(rateio, "valor", "Valor") or 0)
            for rateio in rateios_lancamento
            if self._pick(rateio, "valor", "Valor") is not None
        ]
        total_rateio_explicito = sum(valor_rateios)

        for rateio in rateios_lancamento:
            valor_rateio = self._allocated_value(
                rateio,
                valor_total,
                total_rateio_explicito,
                len(rateios_lancamento),
            )
            categoria_id = self._pick(
                rateio,
                "id_categoria",
                "idcategoria",
                "IdCategoria",
                "categoria_id",
            )
            categoria = categorias_por_id.get(str(categoria_id), {}) if categoria_id else {}

            classificacao = (
                f"{self._pick(categoria, 'tipo', 'Tipo', 'tipo_lancamento', 'TipoLancamento', 'nome', 'Nome') or classificacao_padrao}"
            ).lower()
            compoe_custo = self._pick(categoria, "compoe_custo", "CompoeCusto", "inclui_custo", "IncluiCusto")
            receita, custo, taxa = self._classify_amount(
                valor=valor_rateio,
                classificacao=classificacao,
                compoe_custo=compoe_custo,
            )
            self._apply_amounts(totals, monthly, mes, receita, custo, taxa)

    @staticmethod
    def _apply_amounts(totals, monthly, mes: str, receita: float, custo: float, taxa: float):
        totals["receita"] += receita
        totals["custos"] += custo
        totals["taxas"] += taxa
        monthly[mes]["receita"] += receita
        monthly[mes]["custos"] += custo
        monthly[mes]["taxa"] += taxa

    @staticmethod
    def _allocated_value(rateio, valor_total: float, total_rateio_explicito: float, qtd_rateios: int) -> float:
        valor_rateio = SqlAlchemyFinancialRepository._pick(rateio, "valor", "Valor")
        if valor_rateio is not None:
            return float(valor_rateio)

        percentual = SqlAlchemyFinancialRepository._pick(rateio, "percentual", "Percentual")
        if percentual is not None:
            return valor_total * float(percentual) / 100.0

        if total_rateio_explicito > 0:
            return 0.0
        return valor_total / qtd_rateios if qtd_rateios else valor_total

    @staticmethod
    def _classify_amount(valor: float, classificacao: str, compoe_custo):
        classe = (classificacao or "").lower()
        is_tax = "tax" in classe or "impost" in classe or "tribut" in classe
        is_revenue = "receita" in classe or "credito" in classe or "entrada" in classe

        if is_revenue:
            return valor, 0.0, 0.0
        if is_tax:
            return 0.0, 0.0, valor

        if compoe_custo is None:
            return 0.0, valor, 0.0

        if bool(compoe_custo):
            return 0.0, valor, 0.0
        return 0.0, 0.0, 0.0

    @staticmethod
    def _pick(row, *keys):
        if not row:
            return None
        normalized = {str(key).lower(): value for key, value in row.items()}
        for key in keys:
            if key.lower() in normalized:
                return normalized[key.lower()]
        return None
