from pathlib import Path

from app.ingestion.document_processor import (
    DocumentProcessor,
)

from app.ingestion.chunk_processor import (
    ChunkProcessor,
)


BASE_DIR = Path(__file__).resolve().parent

KNOWLEDGE_BASE_ROOT = (
    BASE_DIR
    / "data"
    / "knowledge_base"
)


def main():

    print()
    print("=" * 80)
    print("PHASE 8 - DOCUMENT CHUNKING")
    print("=" * 80)


    # Load complete documents.

    document_processor = DocumentProcessor(
        knowledge_base_root=(
            KNOWLEDGE_BASE_ROOT
        )
    )


    documents = (
        document_processor.process_all()
    )


    print(
        f"\nDocuments loaded: "
        f"{len(documents)}"
    )


    # Chunk documents.

    chunk_processor = ChunkProcessor(
        max_chunk_chars=1200
    )


    chunks = (
        chunk_processor.process_documents(
            documents
        )
    )


    print(
        f"Chunks created: "
        f"{len(chunks)}"
    )


    # Display chunks.

    for chunk in chunks:

        metadata = chunk.metadata


        print()
        print("-" * 80)

        print(
            f"Chunk ID: "
            f"{metadata.chunk_id}"
        )

        print(
            f"Document: "
            f"{metadata.document_name}"
        )

        print(
            f"Category: "
            f"{metadata.category}"
        )

        print(
            f"Section: "
            f"{metadata.section}"
        )

        print(
            f"Client: "
            f"{metadata.client}"
        )

        print(
            f"District: "
            f"{metadata.district}"
        )

        print(
            f"Asset: "
            f"{metadata.asset_id}"
        )

        print(
            f"Project: "
            f"{metadata.project_id}"
        )

        print(
            f"Characters: "
            f"{len(chunk.text)}"
        )

        print()

        print(chunk.text[:500])


    print()
    print("=" * 80)

    print("PHASE 8 TEST COMPLETE")

    print("=" * 80)


if __name__ == "__main__":
    main()