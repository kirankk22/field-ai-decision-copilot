from pydantic import BaseModel


class Detection(BaseModel):
    id: str
    type: str
    category: str

    latitude: float
    longitude: float

    confidence: float

    observedDate: str

    client: str
    district: str
    assetId: str

    priority: str
    status: str

    description: str