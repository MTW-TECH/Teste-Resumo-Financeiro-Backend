from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, jsonify

from app.application.use_cases.get_company_list import GetCompanyListUseCase
from app.infrastructure.containers import Container
from app.presentation.middleware.auth import require_auth

company_bp = Blueprint("company", __name__, url_prefix="/company")


@company_bp.route("/list", methods=["GET"])
@require_auth
@inject
def get_company_list(
    use_case: GetCompanyListUseCase = Provide[Container.get_company_list_use_case],
):
    companies = use_case.execute()
    return jsonify([asdict(company) for company in companies]), 200
