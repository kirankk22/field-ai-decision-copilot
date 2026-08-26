from fastapi import APIRouter, HTTPException

from app.chat.schemas import (
    ChatMessageRequest,
    ChatMessageResponse,
)

from app.chat.memory import (
    ConversationMemory,
)

from app.chat.follow_up import (
    FollowUpQueryBuilder,
)

from app.services.context_service import (
    build_detection_context,
)

from app.rag.rag_service import (
    RAGService,
)

from llm.llm_client import (
    LLMClient,
)


router = APIRouter(
    prefix="/api/chat",
    tags=["AI Chat"],
)


# ==========================================================
# SHARED SERVICES
# ==========================================================

rag_service = RAGService()

llm_client = LLMClient()

conversation_memory = ConversationMemory()


# ==========================================================
# CHAT ENDPOINT
# ==========================================================

@router.post(
    "",
    response_model=ChatMessageResponse,
)
async def chat(
    request: ChatMessageRequest,
):

    # ======================================================
    # STEP 1
    # LOAD SELECTED DETECTION
    # ======================================================

    context = build_detection_context(
        request.detection_id
    )


    if context is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Detection "
                f"'{request.detection_id}' "
                "not found"
            ),
        )


    detection = context.detection


    # ======================================================
    # STEP 1.5
    # LOAD CONVERSATION HISTORY
    # ======================================================

    history = conversation_memory.get_history(
        request.detection_id
    )


    # ======================================================
    # STEP 2
    # CONVERT DETECTION TO RAG FORMAT
    # ======================================================

    detection_data = {

        "id": detection.id,

        "type": detection.type,

        "confidence": detection.confidence,

        "client": detection.client,

        "district": detection.district,

        "asset_id": detection.assetId,

    }


    # ======================================================
    # STEP 2.5
    # BUILD CONTEXT-AWARE RETRIEVAL QUERY
    # ======================================================

    retrieval_query = (
        FollowUpQueryBuilder.build(
            question=request.message,

            history=history,

            detection=detection_data,
        )
    )


    # ======================================================
    # STEP 3
    # RETRIEVE SCOPED KNOWLEDGE
    # ======================================================

    try:

        results = (
            rag_service.retrieve_context(
                question=request.message,

                client=detection.client,

                district=detection.district,

                asset=detection.assetId,

                top_k=5,

                history=request.history,
            )
        )


        # ==================================================
        # STEP 3.5
        # DETERMINISTIC COST CALCULATION
        # ==================================================

        cost = (
            rag_service.calculate_cost(
                results
            )
        )


    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Knowledge retrieval failed: "
                f"{exc}"
            ),
        ) from exc


    # ======================================================
    # STEP 4
    # BUILD GROUNDED RAG PROMPT
    # ======================================================

    prompt = rag_service.build_prompt(

        question=request.message,

        detection=detection_data,

        results=results,

        cost=cost,

        history=request.history,
    )


    # ======================================================
    # STEP 5
    # CALL LLM
    # ======================================================

    try:

        answer = llm_client.generate(
            prompt
        )


        # ==================================================
        # SAVE CONVERSATION TURN
        # ==================================================

        conversation_memory.add_turn(

            detection_id=request.detection_id,

            user_message=request.message,

            assistant_message=answer,
        )


    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "AI generation failed: "
                f"{exc}"
            ),
        ) from exc


    # ======================================================
    # STEP 6
    # BUILD UNIQUE TRACEABLE SOURCES
    # ======================================================
    #
    # IMPORTANT:
    #
    # We DO NOT deduplicate `results`.
    #
    # The RAG model must continue receiving all retrieved
    # chunks because two chunks from the same document may
    # contain different evidence.
    #
    # We only deduplicate the document list returned to
    # the frontend.
    #
    # Example:
    #
    # Retrieved chunks:
    #
    # 1. Resurfacing_Programme_2027.md
    # 2. ROAD-BBSR-102.md
    # 3. Resurfacing_Programme_2027.md
    # 4. Road_Inspection_Logbook_2026.md
    # 5. Road_Inspection_Logbook_2026.md
    #
    # UI sources:
    #
    # 1. Resurfacing_Programme_2027.md
    # 2. ROAD-BBSR-102.md
    # 3. Road_Inspection_Logbook_2026.md
    #
    # ======================================================

    sources = []

    seen_sources = set()


    for result in results:

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
            or ""
        )


        # ----------------------------------------------
        # Extract folder from document path
        # ----------------------------------------------

        if "/" in document_path:

            folder = (
                document_path
                .rsplit("/", 1)[0]
            )

        else:

            folder = ""


        # ----------------------------------------------
        # Build a stable unique source key.
        #
        # We use both document and folder so that two
        # different documents with the same filename
        # in different folders are not accidentally merged.
        # ----------------------------------------------

        source_key = (
            document_name,
            folder,
        )


        if source_key in seen_sources:

            continue


        seen_sources.add(
            source_key
        )


        sources.append(
            {
                "document":
                    document_name,

                "folder":
                    folder,

                "page":
                    None,
            }
        )


    # ======================================================
    # STEP 7
    # RETURN RESPONSE
    # ======================================================

    return ChatMessageResponse(

        detection_id=
            request.detection_id,

        answer=
            answer,

        cost=
            cost,

        sources=
            sources,
    )