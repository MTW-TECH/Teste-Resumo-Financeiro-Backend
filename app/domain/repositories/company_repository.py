from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.company import Company


class CompanyRepository(ABC):
    """Contract for retrieving company data. Implemented by the infrastructure layer."""

    @abstractmethod
    def get_all(self) -> List[Company]:
        raise NotImplementedError
