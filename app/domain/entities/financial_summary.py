from dataclasses import dataclass


@dataclass(frozen=True)
class FinancialSummary:
    """Represents a snapshot of a company's financial performance."""

    period: str
    currency: str
    revenue: float
    expenses: float
    net_profit: float
    assets: float
    liabilities: float
