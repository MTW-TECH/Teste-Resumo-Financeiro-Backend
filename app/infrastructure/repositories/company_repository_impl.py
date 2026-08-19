from typing import List

from app.domain.entities.company import Company
from app.domain.repositories.company_repository import CompanyRepository


class InMemoryCompanyRepository(CompanyRepository):
    """In-memory implementation, standing in for a database/external API call."""

    _companies = [
        Company(id=1, name="Acme Corp", industry="Manufacturing", founded_year=1985, employee_count=1200),
        Company(id=2, name="Globex Inc", industry="Technology", founded_year=2001, employee_count=450),
        Company(id=3, name="Initech", industry="Finance", founded_year=1998, employee_count=300),
    ]

    def get_all(self) -> List[Company]:
        return list(self._companies)
