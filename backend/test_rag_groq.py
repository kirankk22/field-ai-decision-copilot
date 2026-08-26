from app.rag.rag_service import RAGService
from llm.llm_client import LLMClient


def main():

    print("=" * 80)
    print("PHASE 11.4 - RAG + GROQ TEST")
    print("=" * 80)

    question = (
        "Should we repaint this crossing now "
        "or wait for the planned resurfacing?"
    )

    detection = {
        "id": "DET-001",
        "type": "Faded pedestrian crossing",
        "confidence": 0.94,
        "client": "Demo_Municipal_Corporation",
        "district": "District_3",
        "asset_id": "ROAD-BBSR-102",
    }

    print()
    print("Question:")
    print(question)

    print()
    print("Detection:")
    print(detection)

    rag_service = RAGService()

    print()
    print("Retrieving evidence...")

    results = rag_service.retrieve_context(
        question=question,
        client=detection["client"],
        district=detection["district"],
        asset=detection["asset_id"],
        top_k=5,
    )

    print()
    print(
        f"Retrieved sources: {len(results)}"
    )

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
            f"SOURCE {index}: "
            f"{metadata.get('document_name')}"
        )

        print(
            f"Section: "
            f"{metadata.get('section')}"
        )

        print(
            f"Asset Match: "
            f"{result.get('asset_match', False)}"
        )

    print()
    print("Building RAG prompt...")

    prompt = rag_service.build_prompt(
        question=question,
        detection=detection,
        results=results,
    )

    print()
    print("-" * 80)
    print("PROMPT CREATED")
    print("-" * 80)

    print(prompt)

    print()
    print("Calling Groq...")

    llm_client = LLMClient()

    answer = llm_client.generate(
        prompt
    )

    print()
    print("-" * 80)
    print("GROQ ANSWER")
    print("-" * 80)

    print(answer)

    print()
    print("=" * 80)
    print("PHASE 11.4 TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()