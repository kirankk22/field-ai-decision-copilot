from typing import Any

from app.vectorstore.retriever import ScopedRetriever
from app.rag.prompt_builder import build_rag_prompt

from app.cost.cost_engine import CostEngine
from app.cost.cost_extractor import (
    CostEvidenceExtractor,
)

from app.chat.intent import (
    is_cost_question,
)


class RAGService:
    """
    Coordinates:

    Detection context
        ↓
    Scoped retrieval
        ↓
    Follow-up intent detection
        ↓
    Cost evidence extraction
        ↓
    Deterministic cost calculation
        ↓
    RAG context
        ↓
    Prompt construction
    """

    def __init__(self) -> None:

        self.retriever = ScopedRetriever()


    # ==================================================
    # RETRIEVAL
    # ==================================================

    def retrieve_context(
        self,
        question: str,
        client: str,
        district: str,
        asset: str | None = None,
        top_k: int = 5,
        history: list[dict[str, str]] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Retrieve evidence scoped to the selected
        client, district and optional asset.

        Conversation history is used to understand
        follow-up questions.

        Cost-related follow-ups receive additional
        deterministic retrieval terms so that cost
        evidence is not lost because the user asked
        a short question such as:

            "What would it cost?"
        """

        retrieval_query = self._build_retrieval_query(
            question=question,
            history=history,
        )

        results = self.retriever.search(
            query=retrieval_query,
            client=client,
            district=district,
            asset=asset,
            top_k=top_k,
        )

        # --------------------------------------------------
        # Cost-aware enrichment
        # --------------------------------------------------

        if is_cost_question(question):

            results = self._prioritize_cost_evidence(
                results
            )

        return results


    # ==================================================
    # FOLLOW-UP RETRIEVAL QUERY
    # ==================================================

    @staticmethod
    def _build_retrieval_query(
        question: str,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        """
        Build a retrieval query using the current
        question and relevant conversation context.

        The goal is not to send the entire conversation
        to the embedding model.

        We only add the most recent user/assistant
        context needed to resolve short follow-ups.
        """

        current_question = (
            question
            .strip()
        )

        if not history:

            if is_cost_question(
                current_question
            ):

                return (
                    f"{current_question} "
                    "pedestrian crossing repainting "
                    "unit rate quantity cost"
                )

            return current_question


        recent_messages = history[-4:]

        history_text = []

        for message in recent_messages:

            role = message.get(
                "role",
                "",
            )

            content = message.get(
                "content",
                "",
            )

            if not content:
                continue

            history_text.append(
                f"{role}: {content}"
            )

        if is_cost_question(
            current_question
        ):

            return (
                "\n".join(history_text)
                + "\n"
                + current_question
                + "\n"
                "cost unit rate quantity "
                "pedestrian crossing repainting"
            )

        return (
            "\n".join(history_text)
            + "\n"
            + current_question
        )


    # ==================================================
    # COST EVIDENCE PRIORITIZATION
    # ==================================================

    @staticmethod
    def _prioritize_cost_evidence(
        results: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Move cost-related evidence toward the front
        while preserving the original semantic distance.

        We do not invent evidence.

        We only reorder evidence that was actually
        retrieved from ChromaDB.
        """

        def score(
            result: dict[str, Any],
        ) -> tuple[int, float]:

            metadata = result.get(
                "metadata",
                {},
            )

            document_name = (
                metadata.get(
                    "document_name"
                )
                or ""
            ).lower()

            category = (
                metadata.get(
                    "category"
                )
                or ""
            ).lower()

            section = (
                metadata.get(
                    "section"
                )
                or ""
            ).lower()

            text = (
                result.get(
                    "text",
                    "",
                )
                or ""
            ).lower()

            cost_signal = 0

            if (
                "cost" in category
                or "rate" in category
            ):
                cost_signal += 3

            if (
                "cost" in document_name
                or "rate" in document_name
            ):
                cost_signal += 3

            if (
                "rate" in section
                or "cost" in section
                or "price" in section
            ):
                cost_signal += 3

            if (
                "unit rate" in text
                or "unit_rate" in text
            ):
                cost_signal += 2

            if (
                "eur" in text
                or "quantity" in text
            ):
                cost_signal += 1

            distance = result.get(
                "distance",
                float("inf"),
            )

            return (
                -cost_signal,
                distance,
            )

        return sorted(
            results,
            key=score,
        )


    # ==================================================
    # CONTEXT BUILDING
    # ==================================================

    def build_context(
        self,
        results: list[dict[str, Any]],
    ) -> str:
        """
        Convert retrieved documents into
        traceable RAG evidence.
        """

        if not results:

            return (
                "No supporting documents "
                "were retrieved."
            )

        context_parts = []

        for index, result in enumerate(
            results,
            start=1,
        ):

            metadata = result.get(
                "metadata",
                {},
            )

            document_name = (
                metadata.get(
                    "document_name"
                )
                or "Unknown document"
            )

            document_path = (
                metadata.get(
                    "document_path"
                )
                or "Not specified"
            )

            section = (
                metadata.get(
                    "section"
                )
                or "Not specified"
            )

            category = (
                metadata.get(
                    "category"
                )
                or "Not specified"
            )

            client = (
                metadata.get(
                    "client"
                )
                or "Not specified"
            )

            district = (
                metadata.get(
                    "district"
                )
                or "Not specified"
            )

            asset_id = (
                metadata.get(
                    "asset_id"
                )
                or
                "Not specified at "
                "document/chunk level"
            )

            project_id = (
                metadata.get(
                    "project_id"
                )
                or
                "Not specified at "
                "document/chunk level"
            )

            document_date = (
                metadata.get(
                    "document_date"
                )
                or "Not specified"
            )

            version = (
                metadata.get(
                    "version"
                )
                or "Not specified"
            )

            distance = result.get(
                "distance"
            )

            asset_match = result.get(
                "asset_match",
                False,
            )

            text = result.get(
                "text",
                "",
            )

            context_parts.append(
                f"""
SOURCE {index}

Document:
{document_name}

Path:
{document_path}

Section:
{section}

Category:
{category}

Client:
{client}

District:
{district}

Asset:
{asset_id}

Project:
{project_id}

Document Date:
{document_date}

Version:
{version}

Asset Match:
{asset_match}

Retrieval Distance:
{distance}

Evidence:
{text}
""".strip()
            )

        return "\n\n".join(
            context_parts
        )


    # ==================================================
    # COST CALCULATION
    # ==================================================

    def calculate_cost(
        self,
        results: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        """
        Extract explicit cost evidence and perform
        deterministic calculation.

        Returns None unless both a quantity and
        unit rate are explicitly present.
        """

        evidence = (
            CostEvidenceExtractor
            .extract_from_results(
                results
            )
        )

        if evidence is None:

            return None

        calculation = (
            CostEngine.calculate(

                quantity=evidence[
                    "quantity"
                ],

                unit_rate=evidence[
                    "unit_rate"
                ],

                unit=evidence[
                    "unit"
                ],

                currency=evidence[
                    "currency"
                ],

            )
        )

        return {
            "quantity": (
                calculation.quantity
            ),

            "unit": (
                calculation.unit
            ),

            "unit_rate": (
                calculation.unit_rate
            ),

            "currency": (
                calculation.currency
            ),

            "total_cost": (
                calculation.total_cost
            ),
        }


    # ==================================================
    # PROMPT
    # ==================================================

    def build_prompt(
        self,
        question: str,
        detection: dict[str, Any],
        results: list[dict[str, Any]],
        cost: dict[str, Any] | None = None,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        """
        Build the final grounded prompt.

        If a deterministic cost calculation exists,
        provide it to the prompt as verified data.
        """

        context = self.build_context(
            results
        )

        # --------------------------------------------------
        # Conversation history
        # --------------------------------------------------

        if history:

            history_parts = []

            for message in history[-6:]:

                role = message.get(
                    "role",
                    "",
                )

                content = message.get(
                    "content",
                    "",
                )

                if not content:
                    continue

                history_parts.append(
                    f"{role.upper()}: {content}"
                )

            if history_parts:

                context = (
                    "==================================================\n"
                    "RECENT CONVERSATION\n"
                    "==================================================\n\n"
                    + "\n\n".join(
                        history_parts
                    )
                    + "\n\n"
                    + context
                )


        # --------------------------------------------------
        # Add deterministic cost information
        # --------------------------------------------------

        if cost is not None:

            context += f"""

==================================================
VERIFIED DETERMINISTIC COST CALCULATION
==================================================

The application calculated the following
cost from explicitly retrieved evidence.

Quantity:
{cost["quantity"]} {cost["unit"]}

Unit Rate:
{cost["unit_rate"]:.2f} {cost["currency"]}/{cost["unit"]}

Calculated Total:
{cost["total_cost"]:.2f} {cost["currency"]}

IMPORTANT:

This value was calculated by the application's
deterministic cost engine.

Do NOT recalculate, modify, estimate or invent
another cost value.

Use this calculated value when discussing cost.
""".strip()


        return build_rag_prompt(
            question=question,

            detection=detection,

            context=context,
        )