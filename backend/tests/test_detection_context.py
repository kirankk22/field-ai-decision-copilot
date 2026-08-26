from app.services.context_service import (
    build_detection_context,
)


def test_build_detection_context():
    """
    Verify that a known detection can be loaded
    and converted into the expected application context.
    """

    context = build_detection_context(
        "DET-001"
    )

    assert context is not None

    detection = context.detection

    assert detection.id == "DET-001"

    assert (
        detection.type
        == "Faded pedestrian crossing"
    )

    assert (
        detection.client
        == "Demo Municipal Corporation"
    )

    assert (
        detection.district
        == "District 3"
    )

    assert (
        detection.assetId
        == "ROAD-BBSR-102"
    )

    assert detection.confidence == 0.91


def test_unknown_detection_returns_none():
    """
    Verify that an unknown detection ID
    does not create a fake context.
    """

    context = build_detection_context(
        "DET-999"
    )

    assert context is None