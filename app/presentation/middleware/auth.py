from functools import wraps

import jwt
from dependency_injector.wiring import Provide, inject
from flask import g, jsonify, request

from app.infrastructure.auth.cognito_token_verifier import CognitoTokenVerifier
from app.infrastructure.containers import Container


def require_auth(f):
    """Validates the `Authorization: Bearer <token>` header against Cognito
    and exposes the decoded claims via `flask.g.current_user_claims`."""

    @wraps(f)
    @inject
    def decorated(
        *args,
        token_verifier: CognitoTokenVerifier = Provide[Container.cognito_token_verifier],
        **kwargs,
    ):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing bearer token"}), 401

        token = auth_header.split(" ", 1)[1]
        try:
            g.current_user_claims = token_verifier.verify(token)
        except jwt.PyJWTError as exc:
            return jsonify({"error": f"Invalid token: {exc}"}), 401

        return f(*args, **kwargs)

    return decorated
