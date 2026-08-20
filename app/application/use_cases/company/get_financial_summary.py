from app.domain.entities.financial_summary import FinancialSummary
from app.domain.repositories.financial_repository import FinancialRepository


class GetFinancialSummaryUseCase:

    def __init__(self, financial_repository: FinancialRepository) -> None:
        self._financial_repository = financial_repository

    def execute(self) -> FinancialSummary:
        return self._financial_repository.get_summary()
