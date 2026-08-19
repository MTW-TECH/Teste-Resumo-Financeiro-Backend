from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, jsonify

from app.application.use_cases.get_user_by_id import GetUserByIdUseCase
from app.infrastructure.containers import Container

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/<int:user_id>", methods=["GET"])
@inject
def get_user_by_id(
    user_id: int,
    use_case: GetUserByIdUseCase = Provide[Container.get_user_by_id_use_case],
):
    user = use_case.execute(user_id)
    if user is None:
        return jsonify({"error": f"User with id {user_id} not found"}), 404
    return jsonify(asdict(user)), 200
