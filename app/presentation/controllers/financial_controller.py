from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, jsonify

from app.application.use_cases.get_financial_summary import GetFinancialSummaryUseCase
from app.infrastructure.containers import Container
from app.presentation.middleware.auth import require_auth

financial_bp = Blueprint("financial", __name__, url_prefix="/financial")


@financial_bp.route("/FinancialSummary/", methods=["GET"])
@require_auth
@inject
def get_financial_summary(
    use_case: GetFinancialSummaryUseCase = Provide[Container.get_financial_summary_use_case],
):
    summary = use_case.execute()
    return jsonify(asdict(summary)), 200
