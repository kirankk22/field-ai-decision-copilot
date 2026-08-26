from app.rag.prompt_builder import build_rag_prompt
from app.rag.rag_service import RAGService


def main():

    print()
    print("=" * 80)
    print("PHASE 11 - RAG CONTEXT TEST")
    print("=" * 80)

    detection = {
        "id": "DET-001",
        "type": "Faded pedestrian crossing",
        "confidence": 0.94,
        "client": "Demo_Municipal_Corporation",
        "district": "District_3",
        "asset_id": "ROAD-BBSR-102",
    }

    question = (
        "Should we repaint this crossing now "
        "or wait for the planned resurfacing?"
    )

    rag = RAGService()

    results = rag.retrieve_context(
        question=question,
        client=detection["client"],
        district=detection["district"],
        asset=detection["asset_id"],
        top_k=5,
    )

    print()
    print("Retrieved sources:")
    print("-" * 80)

    for index, result in enumerate(
        results,
        start=1,
    ):

        metadata = result.get(
            "metadata",
            {},
        )

        print()
        print(
            f"{index}. "
            f"{metadata.get('document_name')}"
        )

        print(
            "   Section:",
            metadata.get("section"),
        )

        print(
            "   Asset:",
            metadata.get("asset_id"),
        )

        print(
            "   Project:",
            metadata.get("project_id"),
        )

    context = rag.build_context(
        results
    )

    prompt = build_rag_prompt(
        question=question,
        detection=detection,
        context=context,
    )

    print()
    print("=" * 80)
    print("GENERATED RAG PROMPT")
    print("=" * 80)

    print()
    print(prompt)

    print()
    print("=" * 80)
    print("PHASE 11 CONTEXT TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()