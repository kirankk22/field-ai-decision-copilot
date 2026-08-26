from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    client: str
    district: str
    category: str
    document_name: str
    document_path: str

    version: str | None = None
    document_date: str | None = None

    asset_id: str | None = None
    project_id: str | None = None
    inspection_id: str | None = None
    standard_reference: str | None = None


class IngestedDocument(BaseModel):
    text: str = Field(
        ...,
        description="Full extracted document text",
    )

    metadata: DocumentMetadata


class ChunkMetadata(BaseModel):
    client: str
    district: str
    category: str

    document_name: str
    document_path: str

    chunk_id: str
    chunk_index: int

    section: str | None = None

    version: str | None = None
    document_date: str | None = None

    asset_id: str | None = None
    project_id: str | None = None
    inspection_id: str | None = None
    standard_reference: str | None = None


class DocumentChunk(BaseModel):
    text: str = Field(
        ...,
        description="Retrievable chunk text",
    )

    metadata: ChunkMetadata