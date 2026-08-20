from dataclasses import dataclass
from typing import TypedDict, List


class montlyData(TypedDict):
    mes: str
    receita: int
    custos: int
    taxa: int



@dataclass(frozen=True)
class FinancialSummary:

    receita: str
    custos: str
    taxas: str
    lucro_liquido: str
    ebitda: str
    lucro: str
    lajida: str
    montlyData: List[montlyData]

