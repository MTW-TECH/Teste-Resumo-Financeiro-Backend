import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


class Config:
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    JSON_SORT_KEYS = False

    DATABASE_URL = os.environ.get(
        "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/financial_api"
    )

    # The remote database is reached via discrete host/port/user/password instead of a single URL,
    # so URL.create builds it and safely escapes any special characters in the credentials.
    # render_as_string(hide_password=False) is required: str(URL) masks the password as "***".
    FINANCIAL_REMOTE_DATABASE_URL = (
        URL.create(
            drivername="postgresql+psycopg2",
            username=os.environ.get("FINANCIAL_REMOTE_DB_USER"),
            password=os.environ.get("FINANCIAL_REMOTE_DB_PASSWORD"),
            host=os.environ.get("FINANCIAL_REMOTE_DB_HOST"),
            port=os.environ.get("FINANCIAL_REMOTE_DB_PORT", "5432"),
            database=os.environ.get("FINANCIAL_REMOTE_DB_NAME"),
        ).render_as_string(hide_password=False)
        if os.environ.get("FINANCIAL_REMOTE_DB_HOST")
        else ""
    )

    # Named connections available to DatabaseManager; pass one of these names
    # (e.g. "localdb", "financial_remote") to obtain the matching session factory.
    DATABASE_CONNECTIONS = {
        "localdb": DATABASE_URL,
        "financial_remote": FINANCIAL_REMOTE_DATABASE_URL,
    }


    COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID", "us-east-1_dRwH4FHq3")
    COGNITO_REGION = os.environ.get("COGNITO_REGION", "us-east-1")

    API_VERSION = os.environ.get("API_VERSION", "v1")
