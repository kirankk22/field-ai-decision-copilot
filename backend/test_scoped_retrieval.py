from app.vectorstore.retriever import ScopedRetriever


def main():

    print()
    print("=" * 80)
    print("PHASE 10 - SCOPED RETRIEVAL TEST")
    print("=" * 80)

    retriever = ScopedRetriever()

    query = (
        "Is there a planned road resurfacing "
        "project for this pedestrian crossing?"
    )

    print()
    print("Query:")
    print(query)

    print()
    print("Scope:")
    print("Client: Demo_Municipal_Corporation")
    print("District: District_3")
    print("Asset: ROAD-BBSR-102")

    results = retriever.search(
        query=query,
        client="Demo_Municipal_Corporation",
        district="District_3",
        asset="ROAD-BBSR-102",
        top_k=5,
    )

    print()
    print("-" * 80)
    print("RESULTS")
    print("-" * 80)

    for index, result in enumerate(
        results,
        start=1,
    ):

        metadata = result.get(
            "metadata",
            {},
        )

        print()
        print(f"Result #{index}")
        print("-" * 40)

        print(
            "Document:",
            metadata.get("document_name"),
        )

        print(
            "Category:",
            metadata.get("category"),
        )

        print(
            "Client:",
            metadata.get("client"),
        )

        print(
            "District:",
            metadata.get("district"),
        )

        print(
            "Asset:",
            metadata.get("asset_id"),
        )

        print(
            "Asset Match:",
            result.get("asset_match"),
        )

        print(
            "Distance:",
            result.get("distance"),
        )

        print()

        print(
            result.get("text", "")[:500]
        )

    print()
    print("=" * 80)
    print("PHASE 10 TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()