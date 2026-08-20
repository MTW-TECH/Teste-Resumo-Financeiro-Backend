from dataclasses import dataclass
from typing import TypedDict, List


class RevenueData(TypedDict):
    mes: str
    receita: int
    taxa: int



@dataclass(frozen=True)
class FinancialSummary:
    """Represents a snapshot of a company's financial performance."""

    receita: str
    custos: str
    taxas: str
    lucro: str
    lajida: str
    montlyData: List[RevenueData]

