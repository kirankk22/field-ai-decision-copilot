from app.vectorstore.retriever import ScopedRetriever


def test_scope_normalization():
    """
    Verify conversion from human-readable application
    values to normalized vector-store metadata values.
    """

    assert (
        ScopedRetriever._normalize_scope_value(
            "Demo Municipal Corporation"
        )
        == "Demo_Municipal_Corporation"
    )

    assert (
        ScopedRetriever._normalize_scope_value(
            "District 3"
        )
        == "District_3"
    )

    assert (
        ScopedRetriever._normalize_scope_value(
            "ROAD-BBSR-102"
        )
        == "ROAD-BBSR-102"
    )


def test_scope_normalization_none():
    """
    None should remain None.
    """

    assert (
        ScopedRetriever._normalize_scope_value(
            None
        )
        is None
    )


def test_scoped_retrieval():
    """
    Verify that retrieval returns evidence for the
    selected client and district.
    """

    retriever = ScopedRetriever()

    results = retriever.search(
        query=(
            "planned road resurfacing "
            "pedestrian crossing"
        ),
        client="Demo Municipal Corporation",
        district="District 3",
        asset="ROAD-BBSR-102",
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


def test_asset_match_is_identified():
    """
    Verify that asset-specific evidence is marked
    correctly by the retriever.
    """

    retriever = ScopedRetriever()

    results = retriever.search(
        query=(
            "pedestrian crossing "
            "ROAD-BBSR-102"
        ),
        client="Demo Municipal Corporation",
        district="District 3",
        asset="ROAD-BBSR-102",
        top_k=5,
    )

    asset_matches = [
        result
        for result in results
        if result.get(
            "asset_match",
            False,
        )
    ]

    assert len(asset_matches) > 0