from app.chat.memory import ConversationMemory


def main() -> None:

    print("=" * 80)
    print("PHASE 12.1 - CONVERSATION MEMORY TEST")
    print("=" * 80)


    memory = ConversationMemory()


    detection_id = "DET-001"


    # ==================================================
    # TEST 1
    # EMPTY HISTORY
    # ==================================================

    history = memory.get_history(
        detection_id
    )

    assert history == []

    print()
    print("Initial history:")
    print(history)


    # ==================================================
    # TEST 2
    # ADD FIRST TURN
    # ==================================================

    memory.add_turn(
        detection_id=detection_id,

        user_message=(
            "Should we repaint this crossing "
            "now or wait for the planned resurfacing?"
        ),

        assistant_message=(
            "The evidence supports evaluating "
            "immediate repainting against the "
            "planned resurfacing."
        ),
    )


    history = memory.get_history(
        detection_id
    )


    assert len(history) == 2

    assert history[0]["role"] == "user"

    assert history[1]["role"] == "assistant"


    print()
    print("After first turn:")

    for message in history:

        print(
            f'{message["role"]}: '
            f'{message["content"]}'
        )


    # ==================================================
    # TEST 3
    # ADD FOLLOW-UP
    # ==================================================

    memory.add_turn(
        detection_id=detection_id,

        user_message=(
            "What would it cost?"
        ),

        assistant_message=(
            "The deterministic repainting "
            "cost is 444.00 EUR."
        ),
    )


    history = memory.get_history(
        detection_id
    )


    assert len(history) == 4


    print()
    print("After follow-up:")

    for message in history:

        print(
            f'{message["role"]}: '
            f'{message["content"]}'
        )


    # ==================================================
    # TEST 4
    # DETECTION ISOLATION
    # ==================================================

    det_002_history = memory.get_history(
        "DET-002"
    )


    assert det_002_history == []


    print()
    print(
        "DET-002 history remains isolated:"
    )

    print(det_002_history)


    # ==================================================
    # TEST 5
    # MESSAGE COUNT
    # ==================================================

    count = memory.message_count(
        detection_id
    )


    assert count == 4


    print()
    print(
        f"DET-001 message count: {count}"
    )


    # ==================================================
    # TEST COMPLETE
    # ==================================================

    print()
    print("-" * 80)
    print("PHASE 12.1 TEST PASSED")
    print("=" * 80)


if __name__ == "__main__":
    main()