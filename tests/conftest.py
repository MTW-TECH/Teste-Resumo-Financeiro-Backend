from collections.abc import Iterator
from contextlib import contextmanager
from unittest.mock import Mock

import pytest
from dependency_injector import providers

import config as config_module
from app import create_app


@pytest.fixture
def app():
    # Use in-memory sqlite for tests so app startup does not depend on external services.
    config_module.Config.DATABASE_CONNECTIONS = {
        "localdb": "sqlite+pysqlite:///:memory:",
        "financial_remote": "sqlite+pysqlite:///:memory:",
    }
    flask_app = create_app()
    flask_app.config.update(TESTING=True)
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def token_verifier_mock(app) -> Iterator[Mock]:
    verifier = Mock()
    verifier.verify.return_value = {
        "sub": "cognito-sub-123",
        "email": "john@example.com",
        "name": "John Doe",
    }
    app.container.cognito_token_verifier.override(providers.Object(verifier))
    try:
        yield verifier
    finally:
        app.container.cognito_token_verifier.reset_override()


@contextmanager
def override_provider(container, provider_name: str, value):
    provider = getattr(container, provider_name)
    provider.override(providers.Object(value))
    try:
        yield
    finally:
        provider.reset_override()