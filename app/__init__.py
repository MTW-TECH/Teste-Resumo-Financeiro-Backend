from flask import Flask

from app.infrastructure.containers import Container
from app.presentation.controllers.company_controller import company_bp
from app.presentation.controllers.financial_controller import financial_bp
from app.presentation.controllers.user_controller import user_bp


def create_app() -> Flask:
    container = Container()

    app = Flask(__name__)
    app.config.from_object("config.Config")
    container.config.database_url.from_value(app.config["DATABASE_URL"])
    container.config.cognito_user_pool_id.from_value(app.config["COGNITO_USER_POOL_ID"])
    container.config.cognito_region.from_value(app.config["COGNITO_REGION"])
    app.container = container

    # Eagerly create tables at startup instead of on first repository use.
    container.db_session_factory()

    api_prefix = f"/{app.config['API_VERSION']}"
    for blueprint in (financial_bp, company_bp, user_bp):
        app.register_blueprint(blueprint, url_prefix=f"{api_prefix}{blueprint.url_prefix}")

    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404

    return app
