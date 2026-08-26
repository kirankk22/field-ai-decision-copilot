from app.cost.cost_extractor import (
    CostEvidenceExtractor,
)


def main():

    print("=" * 80)
    print("PHASE 11.5 - COST EVIDENCE EXTRACTION")
    print("=" * 80)


    rate_text = """
    ## Pedestrian Crossing Repainting

    Treatment:

    Pedestrian crossing repainting

    Unit:

    Square metre (m²)

    Unit Rate:

    18.50 EUR / m²
    """


    quantity_text = """
    ## Example Measurement

    Estimated crossing marking area:

    24 m²

    Estimated immediate repainting duration:

    1 day
    """


    rate = (
        CostEvidenceExtractor
        .extract_unit_rate(
            rate_text
        )
    )


    quantity = (
        CostEvidenceExtractor
        .extract_quantity(
            quantity_text
        )
    )


    print()
    print("Extracted Unit Rate:")
    print(rate)

    print()
    print("Extracted Quantity:")
    print(quantity)


    assert rate is not None
    assert rate["unit_rate"] == 18.50
    assert rate["currency"] == "EUR"
    assert rate["unit"] == "m²"

    assert quantity == 24.0


    print()
    print("-" * 80)

    print(
        "COST EXTRACTION TEST PASSED"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()