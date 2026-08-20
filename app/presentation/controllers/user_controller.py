from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, g, jsonify

from app.application.use_cases.user.get_current_user import GetCurrentUserUseCase
from app.application.use_cases.user.get_user_by_id import GetUserByIdUseCase
from app.infrastructure.containers import Container
from app.presentation.middleware.auth import require_auth

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/me", methods=["GET"])
@require_auth
@inject
def get_current_user(
    use_case: GetCurrentUserUseCase = Provide[Container.get_current_user_use_case],
):
    claims = g.current_user_claims
    user = use_case.execute(
        cognito_sub=claims["sub"],
        email=claims.get("email", ""),
        name=claims.get("name", claims.get("username", claims["sub"])),
    )
    return jsonify(asdict(user)), 200


@user_bp.route("/<int:user_id>", methods=["GET"])
@require_auth
@inject
def get_user_by_id(
    user_id: int,
    use_case: GetUserByIdUseCase = Provide[Container.get_user_by_id_use_case],
):
    user = use_case.execute(user_id)
    if user is None:
        return jsonify({"error": f"User with id {user_id} not found"}), 404
    return jsonify(asdict(user)), 200
