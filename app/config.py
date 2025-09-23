import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    PROJECT_NAME: str = "PyQueswers API"
    PROJECT_VERSION: str = "1.0.0"

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/py_queswers_db"
        )

    API_V1_STR: str = "/api/v1"


settings = Settings()
