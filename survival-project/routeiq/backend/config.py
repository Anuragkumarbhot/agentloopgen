import os


class Settings:

    APP_NAME = "AgentLoopGen"

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "production"
    )

    PORT = int(
        os.getenv(
            "PORT",
            "10000"
        )
    )

    DEBUG = os.getenv(
        "DEBUG",
        "false"
    ).lower() == "true"


settings = Settings()
