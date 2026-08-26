from app.rag.rag_service import RAGService


def main():

    print("=" * 80)
    print("PHASE 11.5.2 - RAG + DETERMINISTIC COST")
    print("=" * 80)


    rag = RAGService()


    print()
    print("Retrieving evidence...")


    results = rag.retrieve_context(

        question=(
            "Should we repaint this crossing "
            "now or wait for the planned resurfacing?"
        ),

        client=(
            "Demo Municipal Corporation"
        ),

        district=(
            "District 3"
        ),

        asset=(
            "ROAD-BBSR-102"
        ),

        top_k=5,

    )


    print()
    print(
        f"Retrieved sources: "
        f"{len(results)}"
    )


    for index, result in enumerate(
        results,
        start=1,
    ):

        metadata = result.get(
            "metadata",
            {},
        )

        print(
            f"{index}. "
            f"{metadata.get('document_name')}"
        )


    # ==================================================
    # COST
    # ==================================================

    cost = rag.calculate_cost(
        results
    )


    print()
    print("-" * 80)


    if cost is None:

        print(
            "No deterministic cost "
            "could be calculated."
        )

        raise SystemExit(1)


    print(
        "DETERMINISTIC COST"
    )


    print()
    print(
        f"Quantity: "
        f"{cost['quantity']} "
        f"{cost['unit']}"
    )


    print(
        f"Unit Rate: "
        f"{cost['unit_rate']:.2f} "
        f"{cost['currency']}/{cost['unit']}"
    )


    print(
        f"Total Cost: "
        f"{cost['total_cost']:.2f} "
        f"{cost['currency']}"
    )


    # ==================================================
    # VALIDATION
    # ==================================================

    assert cost["quantity"] == 24.0

    assert cost["unit_rate"] == 18.50

    assert cost["currency"] == "EUR"

    assert cost["total_cost"] == 444.00


    print()
    print("-" * 80)

    print(
        "RAG COST INTEGRATION TEST PASSED"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()