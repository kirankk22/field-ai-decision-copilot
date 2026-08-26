from app.rag.rag_service import RAGService
from app.services.context_service import (
    build_detection_context,
)


QUESTION = (
    "Should we repaint this crossing now "
    "or wait for the planned resurfacing?"
)


def get_detection():
    """
    Load the known test detection used throughout
    the RAG test suite.
    """

    context = build_detection_context(
        "DET-001"
    )

    assert context is not None

    return context.detection


def test_rag_retrieves_scoped_evidence():
    """
    Verify that RAG retrieval returns evidence
    for the selected client, district and asset.
    """

    detection = get_detection()

    service = RAGService()

    results = service.retrieve_context(
        question=QUESTION,
        client=detection.client,
        district=detection.district,
        asset=detection.assetId,
        top_k=5,
    )

    assert isinstance(
        results,
        list,
    )

    assert len(results) > 0

    for result in results:

        metadata = result.get(
            "metadata",
            {},
        )

        assert (
            metadata.get("client")
            == "Demo_Municipal_Corporation"
        )

        assert (
            metadata.get("district")
            == "District_3"
        )


def test_rag_retrieves_resurfacing_programme():
    """
    Verify that the question retrieves the planned
    resurfacing programme evidence.
    """

    detection = get_detection()

    service = RAGService()

    results = service.retrieve_context(
        question=QUESTION,
        client=detection.client,
        district=detection.district,
        asset=detection.assetId,
        top_k=5,
    )

    document_names = [
        result.get(
            "metadata",
            {},
        ).get(
            "document_name"
        )
        for result in results
    ]

    assert (
        "Resurfacing_Programme_2027.md"
        in document_names
    )


def test_rag_retrieves_asset_specific_evidence():
    """
    Verify that an explicitly asset-focused query
    can retrieve asset-specific evidence for
    ROAD-BBSR-102.
    """

    detection = get_detection()

    service = RAGService()

    results = service.retrieve_context(
        question=(
            "What is the asset information for "
            "ROAD-BBSR-102 pedestrian crossing?"
        ),
        client=detection.client,
        district=detection.district,
        asset=detection.assetId,
        top_k=5,
    )

    assert isinstance(
        results,
        list,
    )

    assert len(results) > 0

    asset_matches = [
        result
        for result in results
        if result.get(
            "asset_match",
            False,
        )
    ]

    assert len(asset_matches) > 0

    asset_ids = [
        result.get(
            "metadata",
            {},
        ).get(
            "asset_id"
        )
        for result in asset_matches
    ]

    assert (
        "ROAD-BBSR-102"
        in asset_ids
    )


def test_rag_context_contains_traceable_sources():
    """
    Verify that retrieved evidence is converted
    into traceable RAG context.
    """

    detection = get_detection()

    service = RAGService()

    results = service.retrieve_context(
        question=QUESTION,
        client=detection.client,
        district=detection.district,
        asset=detection.assetId,
        top_k=5,
    )

    context = service.build_context(
        results
    )

    assert "SOURCE 1" in context

    assert (
        "Resurfacing_Programme_2027.md"
        in context
    )

    assert (
        "Demo_Municipal_Corporation"
        in context
    )

    assert (
        "District_3"
        in context
    )

    assert (
        "PRJ-2027-RES-014"
        in context
    )


def test_rag_cost_calculation():
    """
    Verify that RAG retrieves the cost evidence
    and the deterministic cost engine produces
    the expected result.
    """

    detection = get_detection()

    service = RAGService()

    results = service.retrieve_context(
        question=QUESTION,
        client=detection.client,
        district=detection.district,
        asset=detection.assetId,
        top_k=5,
    )

    cost = service.calculate_cost(
        results
    )

    assert cost is not None

    assert cost["quantity"] == 24.0

    assert cost["unit"] == "m²"

    assert cost["unit_rate"] == 18.5

    assert cost["currency"] == "EUR"

    assert cost["total_cost"] == 444.0


def test_rag_prompt_contains_evidence():
    """
    Verify that the final RAG prompt contains
    the detection context and retrieved evidence.
    """

    detection = get_detection()

    detection_data = {
        "id": detection.id,
        "type": detection.type,
        "confidence": detection.confidence,
        "client": detection.client,
        "district": detection.district,
        "asset_id": detection.assetId,
    }

    service = RAGService()

    results = service.retrieve_context(
        question=QUESTION,
        client=detection.client,
        district=detection.district,
        asset=detection.assetId,
        top_k=5,
    )

    cost = service.calculate_cost(
        results
    )

    prompt = service.build_prompt(
        question=QUESTION,
        detection=detection_data,
        results=results,
        cost=cost,
    )

    assert "DET-001" in prompt

    assert (
        "ROAD-BBSR-102"
        in prompt
    )

    assert (
        "Resurfacing_Programme_2027.md"
        in prompt
    )

    assert (
        "PRJ-2027-RES-014"
        in prompt
    )

    assert (
        "444.00 EUR"
        in prompt
    )


def test_rag_prompt_contains_conversation_history():
    """
    Verify that conversation history is accepted
    and included in the generated prompt.
    """

    detection = get_detection()

    detection_data = {
        "id": detection.id,
        "type": detection.type,
        "confidence": detection.confidence,
        "client": detection.client,
        "district": detection.district,
        "asset_id": detection.assetId,
    }

    history = [
        {
            "role": "user",
            "content": (
                "Should we repaint this crossing "
                "now or wait?"
            ),
        },
        {
            "role": "assistant",
            "content": (
                "The crossing is associated "
                "with the planned resurfacing."
            ),
        },
    ]

    service = RAGService()

    results = service.retrieve_context(
        question="What did we discuss earlier?",
        client=detection.client,
        district=detection.district,
        asset=detection.assetId,
        top_k=5,
    )

    prompt = service.build_prompt(
        question="What did we discuss earlier?",
        detection=detection_data,
        results=results,
        history=history,
    )

    assert (
        "Should we repaint this crossing"
        in prompt
    )

    assert (
        "associated with the planned resurfacing"
        in prompt
    )


def test_empty_results_context():
    """
    Verify that an empty retrieval result does not
    produce fabricated evidence.
    """

    service = RAGService()

    context = service.build_context(
        []
    )

    assert (
        context
        == "No supporting documents were retrieved."
    )


def test_empty_results_cost():
    """
    Verify that cost calculation returns None when
    there is no retrieved evidence.
    """

    service = RAGService()

    cost = service.calculate_cost(
        []
    )

    assert cost is None