from typing import List

from sqlalchemy import select

from app.domain.entities.company import Company
from app.domain.repositories.company_repository import CompanyRepository
from app.infrastructure.models.company_model import CompanyModel


class SqlAlchemyCompanyRepository(CompanyRepository):
    """Reads companies from the financial_remote candidato_paulo.empresa view."""

    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def get_all(self) -> List[Company]:
        with self._session_factory() as session:
            models = session.scalars(select(CompanyModel)).all()
            return [self._to_entity(model) for model in models]

    @staticmethod
    def _to_entity(model: CompanyModel) -> Company:
        return Company(
            id=model.id,
            name=model.name,
            cnpj=model.cnpj,
            state=model.state,
            city=model.city,
            active=model.active,
            tax_regime=model.tax_regime,
        )

