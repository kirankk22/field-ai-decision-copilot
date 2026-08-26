from pydantic import BaseModel

from app.models.detection import Detection


class LocationContext(BaseModel):
    latitude: float
    longitude: float
    district: str


class AssetContext(BaseModel):
    id: str


class DetectionContext(BaseModel):
    detection: Detection
    location: LocationContext
    asset: AssetContext