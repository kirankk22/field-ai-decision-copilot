from chromadb.utils.embedding_functions import (
    DefaultEmbeddingFunction,
)


class EmbeddingService:

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):

        self.model_name = model_name

        self.embedding_function = (
            DefaultEmbeddingFunction()
        )

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        embeddings = self.embedding_function(
            texts
        )

        return [
            [float(value) for value in embedding]
            for embedding in embeddings
        ]

    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        embeddings = self.embedding_function(
            [text]
        )

        return [
            float(value)
            for value in embeddings[0]
        ]
