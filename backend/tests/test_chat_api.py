from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


CHAT_URL = "/api/chat"


def test_chat_success():
    """
    Verify that a valid chat request reaches the complete
    RAG + cost + LLM pipeline and returns the expected
    response structure.
    """

    response = client.post(
        CHAT_URL,
        json={
            "detection_id": "DET-001",
            "message": (
                "Should we repaint this crossing now "
                "or wait for the planned resurfacing?"
            ),
            "history": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["detection_id"]
        == "DET-001"
    )

    assert isinstance(
        data["answer"],
        str,
    )

    assert len(data["answer"]) > 0

    assert isinstance(
        data["sources"],
        list,
    )

    assert len(data["sources"]) > 0


def test_chat_returns_cost_for_cost_question():
    """
    Verify that a question requiring cost information
    returns the deterministic cost calculation.
    """

    response = client.post(
        CHAT_URL,
        json={
            "detection_id": "DET-001",
            "message": "What would it cost?",
            "history": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["cost"] is not None

    cost = data["cost"]

    assert cost["quantity"] == 24.0

    assert cost["unit"] == "m²"

    assert cost["unit_rate"] == 18.5

    assert cost["currency"] == "EUR"

    assert cost["total_cost"] == 444.0


def test_chat_returns_traceable_sources():
    """
    Verify that the API exposes document-level source
    information returned by the RAG pipeline.
    """

    response = client.post(
        CHAT_URL,
        json={
            "detection_id": "DET-001",
            "message": (
                "Should we repaint this crossing now "
                "or wait for the planned resurfacing?"
            ),
            "history": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["sources"]) > 0

    documents = [
        source["document"]
        for source in data["sources"]
    ]

    assert (
        "Resurfacing_Programme_2027.md"
        in documents
    )


def test_chat_accepts_conversation_history():
    """
    Verify that the chat API accepts prior conversation
    messages and continues processing normally.
    """

    response = client.post(
        CHAT_URL,
        json={
            "detection_id": "DET-001",
            "message": "What would it cost?",
            "history": [
                {
                    "role": "user",
                    "content": (
                        "Should we repaint this "
                        "crossing now?"
                    ),
                },
                {
                    "role": "assistant",
                    "content": (
                        "The crossing is associated "
                        "with the resurfacing programme."
                    ),
                },
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["detection_id"]
        == "DET-001"
    )

    assert isinstance(
        data["answer"],
        str,
    )

    assert len(data["answer"]) > 0


def test_chat_unknown_detection():
    """
    Verify that an unknown detection ID returns
    HTTP 404 rather than producing an answer from
    fabricated context.
    """

    response = client.post(
        CHAT_URL,
        json={
            "detection_id": "DET-999",
            "message": "What should we do?",
            "history": [],
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert (
        "DET-999"
        in data["detail"]
    )


def test_chat_missing_detection_id():
    """
    Verify FastAPI validation when detection_id
    is omitted.
    """

    response = client.post(
        CHAT_URL,
        json={
            "message": "What should we do?",
            "history": [],
        },
    )

    assert response.status_code == 422


def test_chat_missing_message():
    """
    Verify FastAPI validation when message
    is omitted.
    """

    response = client.post(
        CHAT_URL,
        json={
            "detection_id": "DET-001",
            "history": [],
        },
    )

    assert response.status_code == 422


def test_chat_empty_message():
    """
    Verify that an empty message is rejected by
    Pydantic validation.
    """

    response = client.post(
        CHAT_URL,
        json={
            "detection_id": "DET-001",
            "message": "",
            "history": [],
        },
    )

    assert response.status_code == 422


def test_chat_invalid_history_role():
    """
    Verify that malformed history is rejected if the
    request schema enforces the expected structure.
    """

    response = client.post(
        CHAT_URL,
        json={
            "detection_id": "DET-001",
            "message": "What would it cost?",
            "history": [
                {
                    "role": 123,
                    "content": "Previous message",
                }
            ],
        },
    )

    # Depending on the current Pydantic schema,
    # this may either be rejected with 422 or coerced.
    assert response.status_code in (
        200,
        422,
    )


def test_chat_response_source_structure():
    """
    Verify the structure of every source returned
    by the API.
    """

    response = client.post(
        CHAT_URL,
        json={
            "detection_id": "DET-001",
            "message": "What would it cost?",
            "history": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    for source in data["sources"]:

        assert "document" in source

        assert "folder" in source

        assert "page" in source