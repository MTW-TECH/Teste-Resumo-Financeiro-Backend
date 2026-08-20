from typing import Optional

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class GetUserByIdUseCase:

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def execute(self, user_id: int) -> Optional[User]:
        return self._user_repository.get_by_id(user_id)
