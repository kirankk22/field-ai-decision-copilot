from app.rag.prompt_builder import build_rag_prompt


def test_prompt_contains_detection_context():
    """
    Verify that detection information is included
    in the generated RAG prompt.
    """

    detection = {
        "id": "DET-001",
        "type": "Faded pedestrian crossing",
        "confidence": 0.91,
        "client": "Demo Municipal Corporation",
        "district": "District 3",
        "asset_id": "ROAD-BBSR-102",
    }

    context = """
SOURCE 1

Document:
Resurfacing_Programme_2027.md

Section:
Planned Work

Evidence:
The planned project includes pavement resurfacing.
"""

    prompt = build_rag_prompt(
        question=(
            "Should we repaint this crossing now?"
        ),
        detection=detection,
        context=context,
    )

    assert "DET-001" in prompt

    assert (
        "ROAD-BBSR-102"
        in prompt
    )

    assert (
        "Faded pedestrian crossing"
        in prompt
    )

    assert (
        "Resurfacing_Programme_2027.md"
        in prompt
    )


def test_prompt_contains_grounding_rules():
    """
    Verify that the prompt contains the core
    anti-fabrication / evidence-grounding rules.
    """

    detection = {
        "id": "DET-001",
        "type": "Faded pedestrian crossing",
        "confidence": 0.91,
        "client": "Demo Municipal Corporation",
        "district": "District 3",
        "asset_id": "ROAD-BBSR-102",
    }

    context = """
SOURCE 1

Evidence:
Test evidence.
"""

    prompt = build_rag_prompt(
        question="What should we do?",
        detection=detection,
        context=context,
    )

    assert (
        "Never invent"
        in prompt
    )

    assert (
        "available evidence"
        in prompt
    )