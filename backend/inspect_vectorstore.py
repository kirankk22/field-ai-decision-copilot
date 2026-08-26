import chromadb


VECTOR_STORE_PATH = "data/vectorstore"

COLLECTION_NAME = "field_ai_documents"


def main():

    print()
    print("=" * 80)
    print("VECTOR STORE INSPECTION")
    print("=" * 80)

    client = chromadb.PersistentClient(
        path=VECTOR_STORE_PATH
    )

    print()
    print("Collections:")

    collections = client.list_collections()

    for collection in collections:
        print(
            f"- {collection.name}"
        )

    print()

    try:

        collection = client.get_collection(
            name=COLLECTION_NAME
        )

    except Exception as exc:

        print(
            f"Could not find collection "
            f"'{COLLECTION_NAME}':"
        )

        print(exc)

        return

    print(
        f"Collection: {collection.name}"
    )

    print(
        f"Count: {collection.count()}"
    )

    print()
    print("-" * 80)
    print("SAMPLE RECORDS")
    print("-" * 80)

    results = collection.get(
        limit=10,
        include=[
            "documents",
            "metadatas",
        ],
    )

    documents = results.get(
        "documents",
        [],
    )

    metadatas = results.get(
        "metadatas",
        [],
    )

    ids = results.get(
        "ids",
        [],
    )

    for index, document in enumerate(
        documents
    ):

        print()
        print(
            f"Record #{index + 1}"
        )

        print(
            f"ID: {ids[index]}"
        )

        print(
            f"Metadata: {metadatas[index]}"
        )

        print(
            f"Text: {document[:300]}"
        )

    print()
    print("=" * 80)
    print("INSPECTION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()