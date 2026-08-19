from typing import Optional

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    """In-memory implementation, standing in for a database/external API call."""

    _users = {
        1: User(id=1, name="Alice Johnson", email="alice.johnson@example.com", role="admin"),
        2: User(id=2, name="Bob Smith", email="bob.smith@example.com", role="analyst"),
        3: User(id=3, name="Carol Davis", email="carol.davis@example.com", role="viewer"),
    }

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)
