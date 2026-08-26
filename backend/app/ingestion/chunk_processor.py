from app.ingestion.chunker import (
    split_large_text,
    split_markdown_sections,
)

from app.ingestion.schemas import (
    DocumentChunk,
    ChunkMetadata,
    IngestedDocument,
)


class ChunkProcessor:

    def __init__(
        self,
        max_chunk_chars: int = 1200,
    ):

        self.max_chunk_chars = (
            max_chunk_chars
        )


    def process_document(
        self,
        document: IngestedDocument,
    ) -> list[DocumentChunk]:

        sections = split_markdown_sections(
            document.text
        )


        chunks = []

        chunk_index = 0


        for section_name, section_text in sections:

            section_chunks = split_large_text(
                section_text,
                max_chars=self.max_chunk_chars,
            )


            for section_chunk in section_chunks:

                chunk_id = (
                    f"{document.metadata.document_name}"
                    f":chunk-{chunk_index}"
                )


                metadata = ChunkMetadata(

                    client=(
                        document.metadata.client
                    ),

                    district=(
                        document.metadata.district
                    ),

                    category=(
                        document.metadata.category
                    ),

                    document_name=(
                        document.metadata.document_name
                    ),

                    document_path=(
                        document.metadata.document_path
                    ),

                    chunk_id=chunk_id,

                    chunk_index=chunk_index,

                    section=section_name,

                    version=(
                        document.metadata.version
                    ),

                    document_date=(
                        document.metadata.document_date
                    ),

                    asset_id=(
                        document.metadata.asset_id
                    ),

                    project_id=(
                        document.metadata.project_id
                    ),

                    inspection_id=(
                        document.metadata.inspection_id
                    ),

                    standard_reference=(
                        document.metadata.standard_reference
                    ),
                )


                chunk = DocumentChunk(

                    text=section_chunk,

                    metadata=metadata,
                )


                chunks.append(chunk)

                chunk_index += 1


        return chunks


    def process_documents(
        self,
        documents: list[IngestedDocument],
    ) -> list[DocumentChunk]:

        all_chunks = []


        for document in documents:

            document_chunks = (
                self.process_document(
                    document
                )
            )


            all_chunks.extend(
                document_chunks
            )


        return all_chunks