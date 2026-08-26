from typing import Any


def _format_conversation_history(
    history: list[dict[str, str]] | None,
) -> str:
    """
    Convert conversation history into a readable
    prompt section.

    Conversation history is optional.

    If no history exists, explicitly tell the LLM
    that this is the first question for the detection.
    """

    if not history:

        return (
            "No previous conversation exists "
            "for this detection."
        )


    history_parts = []


    for index, message in enumerate(
        history,
        start=1,
    ):

        role = (
            message.get(
                "role"
            )
            or "unknown"
        )


        content = (
            message.get(
                "content"
            )
            or ""
        )


        history_parts.append(
            f"""
MESSAGE {index}

Role:
{role}

Content:
{content}
""".strip()
        )


    return "\n\n".join(
        history_parts
    )


def build_rag_prompt(
    question: str,
    detection: dict[str, Any],
    context: str,
    history: list[dict[str, str]] | None = None,
) -> str:
    """
    Build the final grounded RAG prompt.

    Includes:

    1. System role
    2. Grounding rules
    3. Detection context
    4. Conversation history
    5. Current question
    6. Retrieved evidence
    7. Answer requirements
    """

    detection_id = (
        detection.get(
            "id"
        )
        or "Not specified"
    )


    detection_type = (
        detection.get(
            "type"
        )
        or "Not specified"
    )


    confidence = detection.get(
        "confidence"
    )


    client = (
        detection.get(
            "client"
        )
        or "Not specified"
    )


    district = (
        detection.get(
            "district"
        )
        or "Not specified"
    )


    asset_id = (
        detection.get(
            "asset_id"
        )
        or "Not specified"
    )


    conversation_history = (
        _format_conversation_history(
            history
        )
    )


    return f"""
You are the Field AI Decision Copilot.

Your role is to provide evidence-grounded
decision support for municipal infrastructure
operations.

You are NOT an autonomous decision maker.

A qualified human professional remains
responsible for the final decision.

==================================================
CORE RULE
==================================================

Answer ONLY from:

1. The selected detection context.
2. The retrieved evidence supplied below.
3. The previous conversation for this same
   detection.

Do not use outside knowledge to fill gaps.

Never invent facts.

Never guess missing values.

==================================================
CONVERSATION MEMORY RULE
==================================================

The conversation history belongs to the
currently selected detection.

Use the history to understand follow-up
questions and references such as:

- "it"
- "this"
- "that"
- "the crossing"
- "the project"
- "the cost"
- "what about waiting?"

Resolve those references using the previous
conversation only when the meaning is clear.

Do not allow previous conversation to override
the current detection context or retrieved
evidence.

If the current question is ambiguous and the
history does not provide enough information,
say so explicitly.

==================================================
DO NOT FABRICATE
==================================================

You must never invent:

- costs
- quantities
- project dates
- project status
- safety percentages
- accident probabilities
- policies
- inspection results
- asset conditions
- maintenance history
- technical standards

If information is unavailable, explicitly say:

"The available evidence does not establish this."

==================================================
DETECTION CONTEXT
==================================================

Detection ID:
{detection_id}

Detection Type:
{detection_type}

Detection Confidence:
{confidence}

Client:
{client}

District:
{district}

Asset:
{asset_id}

==================================================
PREVIOUS CONVERSATION
==================================================

{conversation_history}

==================================================
CURRENT USER QUESTION
==================================================

{question}

==================================================
RETRIEVED EVIDENCE
==================================================

{context}

==================================================
ANSWER REQUIREMENTS
==================================================

Use the previous conversation to understand
follow-up questions.

However, factual claims must remain grounded
in the supplied detection context and retrieved
evidence.

Where appropriate:

1. Explain the assessment.
2. Reference relevant evidence.
3. Compare available options.
4. Provide cost information only when supported.
5. Identify missing information.
6. Identify professional verification required.

Never fabricate information.

If cost information is requested but the
retrieved evidence does not contain the required
rate and quantity, explicitly state that a reliable
numeric cost cannot be established.

If safety consequences are requested but no
validated quantitative safety evidence exists,
provide only a qualitative comparison and clearly
label it as qualitative.

==================================================
SOURCE RULE
==================================================

Important factual statements should be traceable
to the retrieved evidence.

Mention document names and sections when
appropriate.

==================================================
FINAL PRINCIPLE
==================================================

The goal is not to sound confident.

The goal is to provide accurate, traceable and
professionally cautious decision support.

==================================================
END
==================================================
""".strip()