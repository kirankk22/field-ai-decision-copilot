from pathlib import Path

from app.ingestion.document_processor import (
    DocumentProcessor,
)

from app.ingestion.chunk_processor import (
    ChunkProcessor,
)

from app.vectorstore.embeddings import (
    EmbeddingService,
)

from app.vectorstore.chroma_store import (
    ChromaVectorStore,
)


class KnowledgeBaseIndexer:

    def __init__(
        self,
        knowledge_base_root: Path,
        vector_store_path: Path,
    ):

        self.document_processor = (
            DocumentProcessor(
                knowledge_base_root=(
                    knowledge_base_root
                )
            )
        )


        self.chunk_processor = (
            ChunkProcessor(
                max_chunk_chars=1200
            )
        )


        self.embedding_service = (
            EmbeddingService()
        )


        self.vector_store = (
            ChromaVectorStore(
                persist_directory=(
                    vector_store_path
                )
            )
        )


    def build_index(self):

        print(
            "Loading documents..."
        )


        documents = (
            self.document_processor
            .process_all()
        )


        print(
            f"Documents loaded: "
            f"{len(documents)}"
        )


        print(
            "Creating chunks..."
        )


        chunks = (
            self.chunk_processor
            .process_documents(
                documents
            )
        )


        print(
            f"Chunks created: "
            f"{len(chunks)}"
        )


        print(
            "Generating embeddings..."
        )


        texts = [
            chunk.text
            for chunk in chunks
        ]


        embeddings = (
            self.embedding_service
            .embed_documents(
                texts
            )
        )


        print(
            f"Embeddings generated: "
            f"{len(embeddings)}"
        )


        print(
            "Writing to ChromaDB..."
        )


        self.vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
        )


        print(
            "Vector index created."
        )


        print(
            f"Vectors in store: "
            f"{self.vector_store.count()}"
        )


        return {
            "documents": len(documents),
            "chunks": len(chunks),
            "embeddings": len(embeddings),
            "vectors": self.vector_store.count(),
        }