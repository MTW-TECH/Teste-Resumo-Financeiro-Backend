from app.domain.entities.financial_summary import FinancialSummary
from app.domain.repositories.financial_repository import FinancialRepository


class InMemoryFinancialRepository(FinancialRepository):
    """In-memory implementation, standing in for a database/external API call."""

    def get_summary(self) -> FinancialSummary:
        return FinancialSummary(
            period="2026-Q2",
            currency="USD",
            revenue=1_250_000.00,
            expenses=875_000.00,
            net_profit=375_000.00,
            assets=4_200_000.00,
            liabilities=1_800_000.00,
        )
