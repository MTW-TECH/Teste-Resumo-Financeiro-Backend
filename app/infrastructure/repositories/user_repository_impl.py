from typing import Optional

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.models.user_model import UserModel


class SqlAlchemyUserRepository(UserRepository):
    """Persists users in the relational database via SQLAlchemy."""

    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def get_by_id(self, user_id: int) -> Optional[User]:
        with self._session_factory() as session:
            model = session.get(UserModel, user_id)
            return self._to_entity(model) if model else None

    def get_by_cognito_sub(self, cognito_sub: str) -> Optional[User]:
        with self._session_factory() as session:
            model = session.query(UserModel).filter_by(cognito_sub=cognito_sub).first()
            return self._to_entity(model) if model else None

    def upsert_from_claims(self, cognito_sub: str, email: str, name: str) -> User:
        with self._session_factory() as session:
            model = session.query(UserModel).filter_by(cognito_sub=cognito_sub).first()
            if model is None:
                model = UserModel(cognito_sub=cognito_sub, email=email, name=name, role="viewer")
                session.add(model)
            else:
                model.email = email
                model.name = name
            session.commit()
            session.refresh(model)
            return self._to_entity(model)

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            role=model.role,
            cognito_sub=model.cognito_sub,
        )
