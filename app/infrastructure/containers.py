from dependency_injector import containers, providers

from app.application.use_cases.get_company_list import GetCompanyListUseCase
from app.application.use_cases.get_financial_summary import GetFinancialSummaryUseCase
from app.application.use_cases.get_user_by_id import GetUserByIdUseCase
from app.infrastructure.repositories.company_repository_impl import InMemoryCompanyRepository
from app.infrastructure.repositories.financial_repository_impl import InMemoryFinancialRepository
from app.infrastructure.repositories.user_repository_impl import InMemoryUserRepository


class Container(containers.DeclarativeContainer):
    """Central dependency injection wiring: repositories -> use cases -> controllers."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.presentation.controllers.financial_controller",
            "app.presentation.controllers.company_controller",
            "app.presentation.controllers.user_controller",
        ]
    )

    # Infrastructure layer
    financial_repository = providers.Singleton(InMemoryFinancialRepository)
    company_repository = providers.Singleton(InMemoryCompanyRepository)
    user_repository = providers.Singleton(InMemoryUserRepository)

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
