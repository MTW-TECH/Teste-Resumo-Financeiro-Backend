from dependency_injector import containers, providers

from app.application.use_cases.get_company_list import GetCompanyListUseCase
from app.application.use_cases.get_current_user import GetCurrentUserUseCase
from app.application.use_cases.get_financial_summary import GetFinancialSummaryUseCase
from app.application.use_cases.get_user_by_id import GetUserByIdUseCase
from app.infrastructure.auth.cognito_token_verifier import CognitoTokenVerifier
from app.infrastructure.database import create_session_factory
from app.infrastructure.repositories.company_repository_impl import InMemoryCompanyRepository
from app.infrastructure.repositories.financial_repository_impl import InMemoryFinancialRepository
from app.infrastructure.repositories.user_repository_impl import SqlAlchemyUserRepository


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.presentation.controllers.financial_controller",
            "app.presentation.controllers.company_controller",
            "app.presentation.controllers.user_controller",
            "app.presentation.middleware.auth",
        ]
    )

    config = providers.Configuration()

    # Infrastructure layer
    financial_repository = providers.Singleton(InMemoryFinancialRepository)
    company_repository = providers.Singleton(InMemoryCompanyRepository)

    db_session_factory = providers.Singleton(
        create_session_factory,
        database_url=config.database_url,
    )
    user_repository = providers.Singleton(
        SqlAlchemyUserRepository,
        session_factory=db_session_factory,
    )

    cognito_token_verifier = providers.Singleton(
        CognitoTokenVerifier,
        user_pool_id=config.cognito_user_pool_id,
        region=config.cognito_region,
    )

    # Application layer
    get_financial_summary_use_case = providers.Factory(
        GetFinancialSummaryUseCase,
        financial_repository=financial_repository,
    )
    get_company_list_use_case = providers.Factory(
        GetCompanyListUseCase,
        company_repository=company_repository,
    )
    get_user_by_id_use_case = providers.Factory(
        GetUserByIdUseCase,
        user_repository=user_repository,
    )
    get_current_user_use_case = providers.Factory(
        GetCurrentUserUseCase,
        user_repository=user_repository,
    )

