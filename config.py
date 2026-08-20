import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    JSON_SORT_KEYS = False

    DATABASE_URL = os.environ.get(
        "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/financial_api"
    )
    COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID", "us-east-1_dRwH4FHq3")
    COGNITO_REGION = os.environ.get("COGNITO_REGION", "us-east-1")
