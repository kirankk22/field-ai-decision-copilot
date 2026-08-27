from pathlib import Path

from app.vectorstore.indexer import (
    KnowledgeBaseIndexer,
)


from app.vectorstore.chroma_store import (
    ChromaStore,
)


BASE_DIR = Path(__file__).resolve().parent


KNOWLEDGE_BASE_ROOT = (
    BASE_DIR
    / "data"
    / "knowledge_base"
)


VECTOR_STORE_PATH = (
    BASE_DIR
    / "data"
    / "vectorstore"
)


def main():

    print()
    print("=" * 80)
    print("PHASE 9 - EMBEDDINGS + VECTOR STORE")
    print("=" * 80)


    # =========================================
    # BUILD INDEX
    # =========================================

    indexer = KnowledgeBaseIndexer(

        knowledge_base_root=(
            KNOWLEDGE_BASE_ROOT
        ),

        vector_store_path=(
            VECTOR_STORE_PATH
        ),
    )


    result = indexer.build_index()


    print()
    print("-" * 80)

    print(
        "INDEX SUMMARY"
    )

    print(
        f"Documents: "
        f"{result['documents']}"
    )

    print(
        f"Chunks: "
        f"{result['chunks']}"
    )

    print(
        f"Embeddings: "
        f"{result['embeddings']}"
    )

    print(
        f"Vectors: "
        f"{result['vectors']}"
    )


    # =========================================
    # TEST SEMANTIC SEARCH
    # =========================================

    print()
    print("-" * 80)

    print(
        "SEMANTIC SEARCH TEST"
    )

    print("-" * 80)


    vector_store = (
        ChromaStore(
            persist_directory=str(
                VECTOR_STORE_PATH
            )
        )
    )


    query = (
        "Is there a planned road "
        "resurfacing project for this "
        "pedestrian crossing?"
    )


    print()
    print(
        f"Query: {query}"
    )


    results = vector_store.search(
        query=query,
        top_k=5,
    )


    for index, result in enumerate(
        results
    ):

        print()
        print(
            f"Result #{index + 1}"
        )

        print(
            "-" * 40
        )

        metadata = result.get(
            "metadata",
            {},
        )

        document = result.get(
            "text",
            "",
        )

        distance = result.get(
            "distance",
        )

        print(
            f"Document: "
            f"{metadata.get('document_name')}"
        )

        print(
            f"Category: "
            f"{metadata.get('category')}"
        )

        print(
            f"Section: "
            f"{metadata.get('section')}"
        )

        print(
            f"Client: "
            f"{metadata.get('client')}"
        )

        print(
            f"District: "
            f"{metadata.get('district')}"
        )

        print(
            f"Asset: "
            f"{metadata.get('asset_id')}"
        )

        print(
            f"Distance: "
            f"{distance:.4f}"
            if distance is not None
            else "Distance: N/A"
        )

        print()
        print(
            document[:500]
        )


    print()
    print("=" * 80)

    print(
        "PHASE 9 TEST COMPLETE"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()