from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_cognito_sub(self, cognito_sub: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def upsert_from_claims(self, cognito_sub: str, email: str, name: str) -> User:
        raise NotImplementedError
