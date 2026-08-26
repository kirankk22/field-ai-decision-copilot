from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# TEST DATA
# ============================================================

DETECTION_ID = "DET-001"

QUESTION = (
    "Should we repaint this crossing now or wait "
    "for the planned resurfacing?"
)


# ============================================================
# MOCK GROQ RESPONSE
# ============================================================

MOCK_LLM_RESPONSE = """
**1. Assessment**

The detection identifies a faded pedestrian crossing
on asset ROAD-BBSR-102.

The retrieved resurfacing programme includes repainting
degraded pedestrian crossing markings as part of the
planned work.

The available evidence does not establish whether the
crossing should be repainted immediately or deferred,
because the exact resurfacing date and site-specific
visibility and safety information are not available.

**2. Relevant Evidence**

The evidence includes:

- Resurfacing_Programme_2027.md
- Road_Marking_Unit_Rates.md
- Pedestrian_Crossing_Marking_Standard.md

**3. Options**

Act now if professional verification establishes that
the current condition requires immediate intervention.

Wait and coordinate with resurfacing if the crossing
remains acceptable until the planned work.

**4. Cost**

The deterministic cost calculation is:

24 m² × 18.50 EUR/m² = 444.00 EUR.

**5. Missing Information**

The exact resurfacing schedule and site-specific
condition assessment require verification.

**6. Professional Verification**

A qualified municipal professional should verify the
condition, visibility, safety implications and
resurfacing schedule before making the final decision.
""".strip()


# ============================================================
# END-TO-END TEST
# ============================================================


@patch(
    "app.api.chat.llm_client.generate",
    return_value=MOCK_LLM_RESPONSE,
)
def test_complete_decision_support_workflow(
    mock_generate,
):
    """
    Verify the complete business workflow:

    Detection
        ↓
    Detection context
        ↓
    Scoped RAG retrieval
        ↓
    Cost evidence extraction
        ↓
    Deterministic cost calculation
        ↓
    Prompt generation
        ↓
    LLM response
        ↓
    Traceable API response
    """

    response = client.post(
        "/api/chat",
        json={
            "detection_id": DETECTION_ID,
            "message": QUESTION,
            "history": [],
        },
    )

    # --------------------------------------------------------
    # API
    # --------------------------------------------------------

    assert response.status_code == 200

    data = response.json()

    # --------------------------------------------------------
    # Detection
    # --------------------------------------------------------

    assert data["detection_id"] == DETECTION_ID

    # --------------------------------------------------------
    # AI answer
    # --------------------------------------------------------

    assert data["answer"]

    assert (
        "ROAD-BBSR-102"
        in data["answer"]
    )

    assert (
        "444.00"
        in data["answer"]
    )

    # --------------------------------------------------------
    # Deterministic cost
    # --------------------------------------------------------

    assert data["cost"] is not None

    assert (
        data["cost"]["quantity"]
        == 24.0
    )

    assert (
        data["cost"]["unit"]
        == "m²"
    )

    assert (
        data["cost"]["unit_rate"]
        == 18.5
    )

    assert (
        data["cost"]["currency"]
        == "EUR"
    )

    assert (
        data["cost"]["total_cost"]
        == 444.0
    )

    # --------------------------------------------------------
    # Traceable sources
    # --------------------------------------------------------

    assert (
        len(data["sources"])
        > 0
    )

    documents = [
        source["document"]
        for source in data["sources"]
    ]

    assert (
        "Resurfacing_Programme_2027.md"
        in documents
    )

    assert (
        "Road_Marking_Unit_Rates.md"
        in documents
    )

    assert (
        "Pedestrian_Crossing_Marking_Standard.md"
        in documents
    )

    # --------------------------------------------------------
    # Source structure
    # --------------------------------------------------------

    for source in data["sources"]:

        assert "document" in source

        assert "folder" in source

        assert (
            source["document"]
        )

        assert (
            source["folder"]
        )

    # --------------------------------------------------------
    # LLM invocation
    # --------------------------------------------------------

    mock_generate.assert_called_once()


# ============================================================
# COST QUESTION E2E
# ============================================================


@patch(
    "app.api.chat.llm_client.generate",
    return_value=(
        "The verified deterministic cost is "
        "444.00 EUR."
    ),
)
def test_end_to_end_cost_question(
    mock_generate,
):
    """
    Verify that a cost question flows through
    retrieval, deterministic calculation and
    API response.
    """

    response = client.post(
        "/api/chat",
        json={
            "detection_id": DETECTION_ID,
            "message": "What would it cost?",
            "history": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    # --------------------------------------------------------
    # Cost must be present
    # --------------------------------------------------------

    assert data["cost"] is not None

    assert (
        data["cost"]["total_cost"]
        == 444.0
    )

    # --------------------------------------------------------
    # LLM answer
    # --------------------------------------------------------

    assert (
        "444.00 EUR"
        in data["answer"]
    )

    mock_generate.assert_called_once()


# ============================================================
# CONVERSATION CONTINUITY E2E
# ============================================================


@patch(
    "app.api.chat.llm_client.generate",
    return_value=(
        "Based on the previous discussion, "
        "the verified deterministic cost is "
        "444.00 EUR."
    ),
)
def test_end_to_end_conversation_continuity(
    mock_generate,
):
    """
    Verify that conversation history is accepted
    while the current detection and evidence remain
    the grounding context.
    """

    response = client.post(
        "/api/chat",
        json={
            "detection_id": DETECTION_ID,
            "message": "What would it cost?",
            "history": [
                {
                    "role": "user",
                    "content": QUESTION,
                },
                {
                    "role": "assistant",
                    "content": (
                        "The crossing requires "
                        "professional verification "
                        "before deciding."
                    ),
                },
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["detection_id"]
        == DETECTION_ID
    )

    assert (
        data["cost"]["total_cost"]
        == 444.0
    )

    assert (
        "444.00 EUR"
        in data["answer"]
    )

    mock_generate.assert_called_once()