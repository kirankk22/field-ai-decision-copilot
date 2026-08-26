import json
from pathlib import Path

from app.models.detection import Detection


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "detections.json"
)


def load_detections() -> list[Detection]:
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        Detection(**item)
        for item in data
    ]


def get_all_detections() -> list[Detection]:
    return load_detections()


def get_detection_by_id(
    detection_id: str,
) -> Detection | None:

    detections = load_detections()

    for detection in detections:
        if detection.id == detection_id:
            return detection

    return None