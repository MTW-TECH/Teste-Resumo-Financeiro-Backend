import re

from flask import Flask
from flask_cors import CORS

_LOCAL_ORIGIN_PATTERN = re.compile(
    r"^https?://(localhost|127\.0\.0\.1|0\.0\.0\.0)(:\d+)?$"
)


def configure_cors(app: Flask) -> None:
    CORS(
        app,
        origins=_LOCAL_ORIGIN_PATTERN,
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )