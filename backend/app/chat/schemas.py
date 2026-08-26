from pydantic import BaseModel, Field
from typing import Any


class ChatMessageRequest(BaseModel):
    detection_id: str = Field(
        ...,
        description="Selected field detection ID",
    )

    message: str = Field(
        ...,
        min_length=1,
        description="User's question",
    )

    history: list[dict[str, str]] = []


class ChatSource(BaseModel):
    document: str
    folder: str
    page: int | None = None


class ChatCost(BaseModel):
    quantity: float
    unit: str
    unit_rate: float
    currency: str
    total_cost: float


class ChatMessageResponse(BaseModel):
    detection_id: str
    answer: str

    cost: dict[str, Any] | None = None

    sources: list[ChatSource] = []