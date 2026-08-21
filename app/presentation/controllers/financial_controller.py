from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, jsonify

from app.application.use_cases.finantial.get_finantial_summary import GetFinancialSummaryUseCase
from app.infrastructure.containers import Container
from app.presentation.middleware.auth import require_auth

financial_bp = Blueprint("financial", __name__, url_prefix="/financial")


@financial_bp.route("/financialSummary/", methods=["GET"])
@require_auth
@inject
def get_financial_summary(
    use_case: GetFinancialSummaryUseCase = Provide[Container.get_financial_summary_use_case],
):
        """
        Get financial summary
        ---
        tags:
            - Financial
        security:
            - BearerAuth: []
        responses:
            200:
                description: Financial summary returned successfully.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                receita:
                                    type: string
                                custos:
                                    type: string
                                taxas:
                                    type: string
                                lucro_liquido:
                                    type: string
                                ebitda:
                                    type: string
                                lucro:
                                    type: string
                                lajida:
                                    type: string
                                montlyData:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            mes:
                                                type: string
                                            receita:
                                                type: number
                                            custos:
                                                type: number
                                            taxa:
                                                type: number
            401:
                description: Missing or invalid JWT token.
        """
        summary = use_case.execute()
        return jsonify(asdict(summary)), 200
