from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class GetCurrentUserUseCase:

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def execute(self, cognito_sub: str, email: str, name: str) -> User:
        return self._user_repository.upsert_from_claims(cognito_sub, email, name)
