from typing import Any


class ConversationMemory:
    """
    In-memory conversation store.

    Conversations are isolated by detection ID.

    Example:

        DET-001
            user -> question
            assistant -> answer
            user -> follow-up
            assistant -> answer

        DET-002
            user -> question
            assistant -> answer
    """

    def __init__(self) -> None:

        self._conversations: dict[
            str,
            list[dict[str, str]],
        ] = {}


    # ==================================================
    # GET HISTORY
    # ==================================================

    def get_history(
        self,
        detection_id: str,
    ) -> list[dict[str, str]]:
        """
        Return conversation history for a detection.

        A copy is returned so callers cannot directly
        modify the internal memory.
        """

        return list(
            self._conversations.get(
                detection_id,
                [],
            )
        )


    # ==================================================
    # ADD MESSAGE
    # ==================================================

    def add_message(
        self,
        detection_id: str,
        role: str,
        content: str,
    ) -> None:
        """
        Add a message to the conversation.
        """

        if detection_id not in self._conversations:

            self._conversations[
                detection_id
            ] = []


        self._conversations[
            detection_id
        ].append(
            {
                "role": role,
                "content": content,
            }
        )


    # ==================================================
    # ADD COMPLETE TURN
    # ==================================================

    def add_turn(
        self,
        detection_id: str,
        user_message: str,
        assistant_message: str,
    ) -> None:
        """
        Store a complete user/assistant turn.
        """

        self.add_message(
            detection_id=detection_id,
            role="user",
            content=user_message,
        )

        self.add_message(
            detection_id=detection_id,
            role="assistant",
            content=assistant_message,
        )


    # ==================================================
    # CLEAR ONE CONVERSATION
    # ==================================================

    def clear(
        self,
        detection_id: str,
    ) -> None:
        """
        Clear conversation history for one detection.
        """

        self._conversations.pop(
            detection_id,
            None,
        )


    # ==================================================
    # CLEAR ALL CONVERSATIONS
    # ==================================================

    def clear_all(self) -> None:
        """
        Clear every stored conversation.
        """

        self._conversations.clear()


    # ==================================================
    # MESSAGE COUNT
    # ==================================================

    def message_count(
        self,
        detection_id: str,
    ) -> int:
        """
        Return the number of stored messages.
        """

        return len(
            self._conversations.get(
                detection_id,
                [],
            )
        )