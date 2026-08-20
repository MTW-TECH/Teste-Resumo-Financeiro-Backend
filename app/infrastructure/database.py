from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Separate base for models mapped to external/remote databases (e.g. financial_remote views),
# so `create_all` on the local Base never touches tables/views we don't own.
RemoteBase = declarative_base()


def create_session_factory(database_url: str, manage_schema: bool = True):
    """Builds a SQLAlchemy session factory for a single connection.

    Table creation via `create_all` is a dev convenience for databases this app
    owns; use Alembic migrations instead once the schema needs versioned
    changes. Pass `manage_schema=False` for external/remote databases so we
    never attempt to create or alter their schema.
    """
    engine = create_engine(database_url, pool_pre_ping=True)
    if manage_schema:
        Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


class DatabaseManager:
    """Registry of named database connections (e.g. "localdb", "financial_remote").

    Session factories are built lazily on first use and cached, so each named
    connection is instantiated at most once.
    """

    def __init__(self, connections: Dict[str, str]):
        self._connections = connections
        self._session_factories: Dict[str, sessionmaker] = {}

    def get_session_factory(self, name: str, manage_schema: bool = True):
        if name not in self._connections:
            raise ValueError(f"Unknown database connection: {name!r}")
        if name not in self._session_factories:
            self._session_factories[name] = create_session_factory(
                self._connections[name], manage_schema=manage_schema
            )
        return self._session_factories[name]
