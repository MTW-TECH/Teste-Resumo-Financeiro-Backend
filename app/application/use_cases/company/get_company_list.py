from typing import List

from app.domain.entities.company import Company
from app.domain.repositories.company_repository import CompanyRepository


class GetCompanyListUseCase:
    """Orchestrates retrieval of the list of companies."""

    def __init__(self, company_repository: CompanyRepository) -> None:
        self._company_repository = company_repository

    def execute(self) -> List[Company]:
        return self._company_repository.get_all()
