#!/bin/sh

set -e

echo "========================================"
echo "Field AI Decision Copilot"
echo "Container startup"
echo "========================================"

VECTOR_STORE_DIR="/app/data/vectorstore"

echo "Checking vector store..."

VECTOR_COUNT=$(
    python -c "
from app.vectorstore.chroma_store import ChromaStore

store = ChromaStore(
    persist_directory='$VECTOR_STORE_DIR'
)

print(store.collection.count())
"
)

echo "Existing vectors: ${VECTOR_COUNT}"

if [ "$VECTOR_COUNT" -eq 0 ]; then

    echo "Vector store is empty."
    echo "Building knowledge-base index..."

    python -c "
from pathlib import Path
from app.vectorstore.indexer import KnowledgeBaseIndexer

indexer = KnowledgeBaseIndexer(
    knowledge_base_root=Path('/app/data/knowledge_base'),
    vector_store_path=Path('/app/data/vectorstore'),
)

result = indexer.build_index()

print('Indexing result:', result)
"

    echo "Knowledge-base index created."

else

    echo "Existing vector store detected."
    echo "Skipping indexing."

fi

echo "Starting FastAPI..."

exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
