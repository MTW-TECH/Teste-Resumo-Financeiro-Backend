import os


class Config:
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    JSON_SORT_KEYS = False
