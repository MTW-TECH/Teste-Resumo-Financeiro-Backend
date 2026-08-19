from abc import ABC, abstractmethod

from app.domain.entities.financial_summary import FinancialSummary


class FinancialRepository(ABC):
    """Contract for retrieving financial data. Implemented by the infrastructure layer."""

    @abstractmethod
    def get_summary(self) -> FinancialSummary:
        raise NotImplementedError
