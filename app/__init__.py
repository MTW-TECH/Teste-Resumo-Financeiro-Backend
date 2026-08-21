from flask import Flask
from flasgger import Swagger

from app.infrastructure.containers import Container
from app.presentation.controllers.company_controller import company_bp
from app.presentation.controllers.financial_controller import financial_bp
from app.presentation.controllers.user_controller import user_bp
from app.presentation.middleware.cors import configure_cors


def create_app() -> Flask:
    container = Container()

    app = Flask(__name__)
    app.config.from_object("config.Config")
    configure_cors(app)
    container.config.database_connections.from_value(app.config["DATABASE_CONNECTIONS"])
    container.config.cognito_user_pool_id.from_value(app.config["COGNITO_USER_POOL_ID"])
    container.config.cognito_region.from_value(app.config["COGNITO_REGION"])
    app.container = container

    api_version = app.config["API_VERSION"]
    api_prefix = f"/{api_version}"

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "openapi",
                "route": f"{api_prefix}/docs/openapi.json",
                "rule_filter": lambda rule: rule.rule.startswith(api_prefix),
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": f"{api_prefix}/docs/",
    }
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Financial Flask API",
            "version": api_version,
            "description": "API documentation for Financial Flask API.",
        },
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}".',
            }
        },
    }
    Swagger(app, config=swagger_config, template=swagger_template)

    # Eagerly create localdb tables at startup; financial_remote connects lazily on first use.
    container.localdb_session_factory()

    for blueprint in (financial_bp, company_bp, user_bp):
        app.register_blueprint(blueprint, url_prefix=f"{api_prefix}{blueprint.url_prefix}")

    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404

    return app
