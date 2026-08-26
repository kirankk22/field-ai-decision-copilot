import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    """
    Application configuration loaded from environment variables.

    The same configuration class is used for both development
    and production environments.
    """

    def __init__(self) -> None:

        self.app_name = os.getenv(
            "APP_NAME",
            "Field AI Decision Copilot",
        )

        self.app_env = os.getenv(
            "APP_ENV",
            "development",
        ).strip().lower()

        self.debug = self._parse_bool(
            os.getenv(
                "DEBUG",
                "false",
            )
        )

        self.cors_origins = (
            self._parse_cors_origins()
        )


    # ==================================================
    # BOOLEAN PARSING
    # ==================================================

    @staticmethod
    def _parse_bool(
        value: str,
    ) -> bool:
        """
        Convert an environment value into a boolean.

        Accepted true values:

            true
            1
            yes
            on

        Everything else is treated as false.
        """

        return (
            value
            .strip()
            .lower()
            in {
                "true",
                "1",
                "yes",
                "on",
            }
        )


    # ==================================================
    # CORS
    # ==================================================

    @staticmethod
    def _parse_cors_origins() -> list[str]:
        """
        Read comma-separated frontend origins.

        Example:

            CORS_ORIGINS=http://localhost:5174,https://example.com
        """

        value = os.getenv(
            "CORS_ORIGINS",
            "",
        )

        return [
            origin.strip()
            for origin in value.split(",")
            if origin.strip()
        ]


settings = Settings()
