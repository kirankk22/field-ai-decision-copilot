from pathlib import Path

from app.vectorstore.indexer import (
    KnowledgeBaseIndexer,
)

from app.vectorstore.embeddings import (
    EmbeddingService,
)

from app.vectorstore.chroma_store import (
    ChromaVectorStore,
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


    embedding_service = (
        EmbeddingService()
    )


    vector_store = (
        ChromaVectorStore(
            persist_directory=(
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


    query_embedding = (
        embedding_service
        .embed_query(query)
    )


    results = (
        vector_store.search(
            query_embedding=query_embedding,
            n_results=5,
        )
    )


    documents = (
        results.get(
            "documents",
            [[]],
        )[0]
    )


    metadatas = (
        results.get(
            "metadatas",
            [[]],
        )[0]
    )


    distances = (
        results.get(
            "distances",
            [[]],
        )[0]
    )


    for index, document in enumerate(
        documents
    ):

        print()
        print(
            f"Result #{index + 1}"
        )

        print(
            "-" * 40
        )


        metadata = metadatas[index]


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
            f"{distances[index]:.4f}"
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