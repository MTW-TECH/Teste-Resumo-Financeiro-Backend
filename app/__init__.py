from flask import Flask

from app.infrastructure.containers import Container
from app.presentation.controllers.company_controller import company_bp
from app.presentation.controllers.financial_controller import financial_bp
from app.presentation.controllers.user_controller import user_bp


def create_app() -> Flask:
    container = Container()

    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.container = container

    app.register_blueprint(financial_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(user_bp)

    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404

    return app
