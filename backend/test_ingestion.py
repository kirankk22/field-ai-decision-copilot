from pathlib import Path

from app.ingestion.document_processor import (
    DocumentProcessor,
)


BASE_DIR = Path(__file__).resolve().parent

KNOWLEDGE_BASE_ROOT = (
    BASE_DIR
    / "data"
    / "knowledge_base"
)


def main():

    processor = DocumentProcessor(
        knowledge_base_root=(
            KNOWLEDGE_BASE_ROOT
        )
    )


    documents = processor.process_all()


    print()
    print("=" * 70)
    print("KNOWLEDGE BASE INGESTION")
    print("=" * 70)


    print(
        f"\nDocuments discovered: "
        f"{len(documents)}"
    )


    for index, document in enumerate(
        documents,
        start=1,
    ):

        metadata = document.metadata


        print()
        print("-" * 70)

        print(
            f"Document #{index}"
        )

        print(
            f"Name: "
            f"{metadata.document_name}"
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
            f"Category: "
            f"{metadata.category}"
        )

        print(
            f"Asset ID: "
            f"{metadata.asset_id}"
        )

        print(
            f"Project ID: "
            f"{metadata.project_id}"
        )

        print(
            f"Inspection ID: "
            f"{metadata.inspection_id}"
        )

        print(
            f"Standard: "
            f"{metadata.standard_reference}"
        )

        print(
            f"Characters: "
            f"{len(document.text)}"
        )


    print()
    print("=" * 70)


if __name__ == "__main__":
    main()