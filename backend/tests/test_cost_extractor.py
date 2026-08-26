from app.cost.cost_extractor import CostEvidenceExtractor


def test_extract_cost_evidence():
    """
    Verify that explicit quantity and unit-rate
    evidence can be extracted.
    """

    results = [
        {
            "metadata": {
                "document_name": "Road_Marking_Unit_Rates.md",
                "section": "Pedestrian Crossing Repainting",
            },
            "text": """
            Treatment:

            Pedestrian crossing repainting

            Unit:

            Square metre (m²)

            Unit Rate:

            18.50 EUR / m²
            """,
        },
        {
            "metadata": {
                "document_name": "Road_Marking_Unit_Rates.md",
                "section": "Example Measurement",
            },
            "text": """
            Estimated crossing marking area:

            24 m²
            """,
        },
    ]

    evidence = (
        CostEvidenceExtractor
        .extract_from_results(results)
    )

    assert evidence is not None

    assert evidence["unit_rate"] == 18.5
    assert evidence["currency"] == "EUR"
    assert evidence["unit"] == "m²"
    assert evidence["quantity"] == 24.0


def test_extract_cost_evidence_missing_quantity():
    """
    Verify that extraction does not produce a
    complete cost calculation when quantity is absent.
    """

    results = [
        {
            "metadata": {
                "document_name": "Road_Marking_Unit_Rates.md",
                "section": "Pedestrian Crossing Repainting",
            },
            "text": """
            Unit Rate:

            18.50 EUR / m²
            """,
        }
    ]

    evidence = (
        CostEvidenceExtractor
        .extract_from_results(results)
    )

    assert evidence is None