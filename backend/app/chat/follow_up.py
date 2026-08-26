from __future__ import annotations

from typing import Any


class FollowUpQueryBuilder:
    """
    Builds a retrieval query for conversational follow-up
    questions.

    The purpose of this class is to make retrieval
    conversation-aware without asking the LLM to
    rewrite the query.

    Example:

        Previous user:
        Should we repaint this crossing?

        Previous assistant:
        The crossing is 24 m² and the unit rate is
        18.50 EUR/m².

        Current user:
        What would it cost?

    Retrieval query becomes a contextual query containing
    the current question plus relevant previous context.
    """

    MAX_HISTORY_TURNS = 4
    MAX_ASSISTANT_CHARS = 3000
    MAX_USER_CHARS = 500

    @classmethod
    def build(
        cls,
        question: str,
        history: list[dict[str, str]] | None,
        detection: dict[str, Any],
    ) -> str:
        """
        Build a deterministic context-aware retrieval query.

        No LLM is used here.

        The query contains:

        1. Current user question
        2. Detection context
        3. Recent conversation turns
        """

        parts: list[str] = []

        # ==================================================
        # CURRENT QUESTION
        # ==================================================

        current_question = (
            question or ""
        ).strip()

        if current_question:

            parts.append(
                f"Current question:\n"
                f"{current_question}"
            )

        # ==================================================
        # DETECTION CONTEXT
        # ==================================================

        detection_id = detection.get(
            "id"
        )

        detection_type = detection.get(
            "type"
        )

        asset_id = detection.get(
            "asset_id"
        )

        client = detection.get(
            "client"
        )

        district = detection.get(
            "district"
        )

        detection_parts = []

        if detection_id:
            detection_parts.append(
                f"Detection ID: {detection_id}"
            )

        if detection_type:
            detection_parts.append(
                f"Detection type: {detection_type}"
            )

        if asset_id:
            detection_parts.append(
                f"Asset: {asset_id}"
            )

        if client:
            detection_parts.append(
                f"Client: {client}"
            )

        if district:
            detection_parts.append(
                f"District: {district}"
            )

        if detection_parts:

            parts.append(
                "Detection context:\n"
                + "\n".join(
                    detection_parts
                )
            )

        # ==================================================
        # CONVERSATION HISTORY
        # ==================================================

        if history:

            recent_history = history[
                -cls.MAX_HISTORY_TURNS:
            ]

            history_parts = []

            for turn in recent_history:

                role = (
                    turn.get("role", "")
                    .strip()
                    .lower()
                )

                content = (
                    turn.get("content", "")
                    .strip()
                )

                if not content:
                    continue

                # ------------------------------------------
                # USER MESSAGE
                # ------------------------------------------

                if role == "user":

                    content = content[
                        :cls.MAX_USER_CHARS
                    ]

                    history_parts.append(
                        "Previous user question:\n"
                        + content
                    )

                # ------------------------------------------
                # ASSISTANT MESSAGE
                # ------------------------------------------

                elif role == "assistant":

                    content = content[
                        :cls.MAX_ASSISTANT_CHARS
                    ]

                    history_parts.append(
                        "Previous assistant evidence:\n"
                        + content
                    )

            if history_parts:

                parts.append(
                    "Recent conversation context:\n"
                    + "\n\n".join(
                        history_parts
                    )
                )

        # ==================================================
        # FINAL QUERY
        # ==================================================

        return "\n\n".join(parts).strip()