from typing import Any

import chromadb

from app.vectorstore.embeddings import EmbeddingService


class ChromaStore:

    def __init__(
        self,
        collection_name: str = "field_ai_documents",
        persist_directory: str = "data/vectorstore",
    ):

        self.embedding_service = EmbeddingService()

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

    def add_documents(
        self,
        documents: list[dict[str, Any]],
    ) -> None:

        if not documents:
            return

        texts = [
            document["text"]
            for document in documents
        ]

        ids = [
            document["id"]
            for document in documents
        ]

        metadatas = [
            document["metadata"]
            for document in documents
        ]

        embeddings = (
            self.embedding_service.embed_documents(
                texts
            )
        )

        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:

        query_embedding = (
            self.embedding_service.embed_query(
                query
            )
        )

        search_arguments: dict[str, Any] = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
        }

        # -------------------------------------------------
        # ChromaDB metadata filtering
        #
        # ChromaDB requires $and when multiple metadata
        # conditions are supplied.
        # -------------------------------------------------

        if filters:

            filter_conditions = []

            for key, value in filters.items():

                if value is not None:

                    filter_conditions.append(
                        {
                            key: value
                        }
                    )

            if len(filter_conditions) == 1:

                search_arguments["where"] = (
                    filter_conditions[0]
                )

            elif len(filter_conditions) > 1:

                search_arguments["where"] = {
                    "$and": filter_conditions
                }

        results = self.collection.query(
            **search_arguments
        )

        documents = (
            results.get("documents", [[]])[0]
        )

        metadatas = (
            results.get("metadatas", [[]])[0]
        )

        distances = (
            results.get("distances", [[]])[0]
        )

        output = []

        for index, document in enumerate(
            documents
        ):

            metadata = (
                metadatas[index]
                if index < len(metadatas)
                else {}
            )

            distance = (
                distances[index]
                if index < len(distances)
                else None
            )

            output.append(
                {
                    "text": document,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

        return output