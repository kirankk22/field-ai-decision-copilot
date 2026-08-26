from app.chat.follow_up import (
    FollowUpQueryBuilder,
)


def main():

    print("=" * 80)
    print(
        "PHASE 12.3 - "
        "CONTEXT-AWARE FOLLOW-UP RETRIEVAL TEST"
    )
    print("=" * 80)


    detection = {

        "id": "DET-001",

        "type": "Faded pedestrian crossing",

        "confidence": 0.91,

        "client": (
            "Demo Municipal Corporation"
        ),

        "district": "District 3",

        "asset_id": "ROAD-BBSR-102",
    }


    history = [

        {
            "role": "user",

            "content": (
                "Should we repaint this crossing "
                "now or wait for the planned "
                "resurfacing?"
            ),
        },

        {
            "role": "assistant",

            "content": (
                "The crossing has a documented "
                "example measurement of 24 m². "
                "The applicable repainting unit "
                "rate is 18.50 EUR/m²."
            ),
        },
    ]


    question = (
        "What would it cost?"
    )


    query = FollowUpQueryBuilder.build(

        question=question,

        history=history,

        detection=detection,
    )


    print()
    print("CURRENT QUESTION")
    print("-" * 80)
    print(question)


    print()
    print("GENERATED RETRIEVAL QUERY")
    print("-" * 80)
    print(query)


    # ==================================================
    # VALIDATION
    # ==================================================

    assert (
        "What would it cost?"
        in query
    )

    assert (
        "ROAD-BBSR-102"
        in query
    )

    assert (
        "24 m²"
        in query
    )

    assert (
        "18.50 EUR/m²"
        in query
    )


    print()
    print("-" * 80)
    print(
        "PHASE 12.3 QUERY TEST PASSED"
    )
    print("=" * 80)


if __name__ == "__main__":
    main()