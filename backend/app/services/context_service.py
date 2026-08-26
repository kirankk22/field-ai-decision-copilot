from app.models.context import (
    AssetContext,
    DetectionContext,
    LocationContext,
)

from app.services.detection_service import (
    get_detection_by_id,
)


def build_detection_context(
    detection_id: str,
) -> DetectionContext | None:

    detection = get_detection_by_id(
        detection_id
    )

    if detection is None:
        return None

    location = LocationContext(
        latitude=detection.latitude,
        longitude=detection.longitude,
        district=detection.district,
    )

    asset = AssetContext(
        id=detection.assetId
    )

    return DetectionContext(
        detection=detection,
        location=location,
        asset=asset,
    )