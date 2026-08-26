from fastapi import APIRouter, HTTPException

from app.models.context import DetectionContext
from app.models.detection import Detection

from app.services.context_service import (
    build_detection_context,
)

from app.services.detection_service import (
    get_all_detections,
    get_detection_by_id,
)


router = APIRouter(
    prefix="/api/detections",
    tags=["Detections"],
)


@router.get(
    "",
    response_model=list[Detection],
)
async def list_detections():

    return get_all_detections()


@router.get(
    "/{detection_id}",
    response_model=Detection,
)
async def get_detection(
    detection_id: str,
):

    detection = get_detection_by_id(
        detection_id
    )

    if detection is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Detection '{detection_id}' "
                "not found"
            ),
        )

    return detection


@router.get(
    "/{detection_id}/context",
    response_model=DetectionContext,
)
async def get_detection_context(
    detection_id: str,
):

    context = build_detection_context(
        detection_id
    )

    if context is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Detection '{detection_id}' "
                "not found"
            ),
        )

    return context