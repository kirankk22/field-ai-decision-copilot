from app.config import Settings, settings


def test_settings_has_application_name():
    assert settings.app_name == "Field AI Decision Copilot"


def test_settings_has_environment():
    assert settings.app_env


def test_settings_debug_is_boolean():
    assert isinstance(
        settings.debug,
        bool,
    )


def test_settings_has_cors_origins():
    assert isinstance(
        settings.cors_origins,
        list,
    )

    assert len(
        settings.cors_origins
    ) > 0


# ==================================================
# BOOLEAN PARSING
# ==================================================


def test_settings_parse_bool_true_values():

    true_values = [
        "true",
        "TRUE",
        "1",
        "yes",
        "YES",
        "on",
        "ON",
    ]

    for value in true_values:

        assert (
            Settings._parse_bool(value)
            is True
        )


def test_settings_parse_bool_false_values():

    false_values = [
        "false",
        "FALSE",
        "0",
        "no",
        "NO",
        "off",
        "OFF",
        "",
        "random",
    ]

    for value in false_values:

        assert (
            Settings._parse_bool(value)
            is False
        )


# ==================================================
# CORS PARSING
# ==================================================


def test_settings_parse_cors_origins():

    import os

    original = os.environ.get(
        "CORS_ORIGINS"
    )

    try:

        os.environ[
            "CORS_ORIGINS"
        ] = (
            "http://localhost:5174, "
            "http://127.0.0.1:5174, "
            "https://example.com"
        )

        origins = (
            Settings._parse_cors_origins()
        )

        assert origins == [
            "http://localhost:5174",
            "http://127.0.0.1:5174",
            "https://example.com",
        ]

    finally:

        if original is None:

            os.environ.pop(
                "CORS_ORIGINS",
                None,
            )

        else:

            os.environ[
                "CORS_ORIGINS"
            ] = original


def test_settings_parse_empty_cors_origins():

    import os

    original = os.environ.get(
        "CORS_ORIGINS"
    )

    try:

        os.environ[
            "CORS_ORIGINS"
        ] = ""

        origins = (
            Settings._parse_cors_origins()
        )

        assert origins == []

    finally:

        if original is None:

            os.environ.pop(
                "CORS_ORIGINS",
                None,
            )

        else:

            os.environ[
                "CORS_ORIGINS"
            ] = original
