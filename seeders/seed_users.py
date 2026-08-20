"""Seed script for the `users` table.

Usage:
    python -m seeders.seed_users
"""
import os

from app.infrastructure.database import create_session_factory
from app.infrastructure.models.user_model import UserModel

USERS = [
    {
        "name": "paulo test",
        "email": "test@example.com",
        "role": "user",
        "cognito_sub": "example-sub",
    },
]


def seed() -> None:
    database_url = os.environ.get(
        "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/financial_api"
    )
    session_factory = create_session_factory(database_url)
    session = session_factory()

    try:
        for user_data in USERS:
            # cognito_sub is the natural key: avoids clashing with real, DB-assigned ids.
            existing = (
                session.query(UserModel)
                .filter_by(cognito_sub=user_data["cognito_sub"])
                .first()
            )
            if existing is not None:
                continue
            session.add(UserModel(**user_data))
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    seed()
