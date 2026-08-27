from pathlib import Path

from app.ingestion.document_processor import DocumentProcessor
from app.ingestion.chunk_processor import ChunkProcessor
from app.vectorstore.embeddings import EmbeddingService
from app.vectorstore.chroma_store import ChromaStore


class KnowledgeBaseIndexer:

    def __init__(
        self,
        knowledge_base_root: Path,
        vector_store_path: Path,
    ):
        self.document_processor = DocumentProcessor(
            knowledge_base_root=knowledge_base_root
        )

        self.chunk_processor = ChunkProcessor(
            max_chunk_chars=1200
        )

        self.embedding_service = EmbeddingService()

        self.vector_store = ChromaStore(
            persist_directory=str(vector_store_path)
        )

    def build_index(self):

        print("Loading documents...")

        documents = self.document_processor.process_all()

        print(
            f"Documents loaded: {len(documents)}"
        )

        print("Creating chunks...")

        chunks = self.chunk_processor.process_documents(
            documents
        )

        print(
            f"Chunks created: {len(chunks)}"
        )

        print("Generating embeddings...")

        texts = [
            chunk.text
            for chunk in chunks
        ]

        embeddings = self.embedding_service.embed_documents(
            texts
        )

        print(
            f"Embeddings generated: {len(embeddings)}"
        )

        print("Writing to ChromaDB...")

        documents_for_store = [
            {
                "id": chunk.metadata.chunk_id,
                "text": chunk.text,
                "metadata": chunk.metadata.model_dump(
                    exclude_none=True
                ),
            }
            for chunk in chunks
        ]

        self.vector_store.collection.upsert(
            ids=[
                document["id"]
                for document in documents_for_store
            ],
            documents=[
                document["text"]
                for document in documents_for_store
            ],
            metadatas=[
                document["metadata"]
                for document in documents_for_store
            ],
            embeddings=embeddings,
        )

        vector_count = self.vector_store.collection.count()

        print("Vector index created.")

        print(
            f"Vectors in store: {vector_count}"
        )

        return {
            "documents": len(documents),
            "chunks": len(chunks),
            "embeddings": len(embeddings),
            "vectors": vector_count,
        }
