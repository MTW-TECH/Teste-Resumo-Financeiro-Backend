from dependency_injector import containers, providers

from app.application.use_cases.company.get_company_list import GetCompanyListUseCase
from app.application.use_cases.company.get_financial_summary import GetFinancialSummaryUseCase
from app.application.use_cases.user.get_current_user import GetCurrentUserUseCase
from app.application.use_cases.user.get_user_by_id import GetUserByIdUseCase
from app.infrastructure.auth.cognito_token_verifier import CognitoTokenVerifier
from app.infrastructure.database import DatabaseManager
from app.infrastructure.repositories.company_repository_impl import SqlAlchemyCompanyRepository
from app.infrastructure.repositories.financial_repository_impl import InMemoryFinancialRepository
from app.infrastructure.repositories.user_repository_impl import SqlAlchemyUserRepository


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.presentation.controllers.financial_controller",
            "app.presentation.controllers.company_controller",
            "app.presentation.controllers.user_controller",
            "app.presentation.middleware.auth",
            "app.presentation.middleware.cors",
        ]
    )

    config = providers.Configuration()

    # Registry of named database connections (e.g. "localdb", "financial_remote"); pass a
    # connection name to `database_manager.get_session_factory(...)` to obtain that database's
    # session factory, built lazily on first use.
    database_manager = providers.Singleton(
        DatabaseManager,
        connections=config.database_connections,
    )
    localdb_session_factory = providers.Singleton(
        lambda db_manager: db_manager.get_session_factory("localdb", manage_schema=True),
        db_manager=database_manager,
    )
    # manage_schema=False: this is an external database we don't own, so we never create/alter its tables.
    financial_remote_session_factory = providers.Singleton(
        lambda db_manager: db_manager.get_session_factory("financial_remote", manage_schema=False),
        db_manager=database_manager,
    )

    # Infrastructure layer: singletons are wired from a (class, kwargs) table.
    # A string value means "use the already-built singleton with this name" instead of a literal/config value.
    _SINGLETONS = {
        "financial_repository": (InMemoryFinancialRepository, {}),
        "company_repository": (SqlAlchemyCompanyRepository, {"session_factory": "financial_remote_session_factory"}),
        "user_repository": (SqlAlchemyUserRepository, {"session_factory": "localdb_session_factory"}),
        "cognito_token_verifier": (
            CognitoTokenVerifier,
            {"user_pool_id": config.cognito_user_pool_id, "region": config.cognito_region},
        ),
    }
    for _name, (_cls, _kwargs) in _SINGLETONS.items():
        _resolved_kwargs = {
            key: (locals()[value] if isinstance(value, str) else value)
            for key, value in _kwargs.items()
        }
        locals()[_name] = providers.Singleton(_cls, **_resolved_kwargs)
    del _SINGLETONS, _name, _cls, _kwargs, _resolved_kwargs

    # Application layer: use cases are wired from a (class, repository kwarg, repository provider) table
    _USE_CASES = {
        "get_financial_summary_use_case": (GetFinancialSummaryUseCase, "financial_repository", financial_repository),
        "get_company_list_use_case": (GetCompanyListUseCase, "company_repository", company_repository),
        "get_user_by_id_use_case": (GetUserByIdUseCase, "user_repository", user_repository),
        "get_current_user_use_case": (GetCurrentUserUseCase, "user_repository", user_repository),
    }
    for _name, (_use_case_cls, _repo_kwarg, _repo_provider) in _USE_CASES.items():
        locals()[_name] = providers.Factory(_use_case_cls, **{_repo_kwarg: _repo_provider})
    del _USE_CASES, _name, _use_case_cls, _repo_kwarg, _repo_provider

