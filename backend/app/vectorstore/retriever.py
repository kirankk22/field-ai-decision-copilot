from typing import Any

from app.vectorstore.chroma_store import ChromaStore


class ScopedRetriever:
    """
    Retrieves knowledge from ChromaDB while enforcing
    client, district and optional asset scope.

    Human-readable application values are normalized
    before they are used as ChromaDB metadata filters.
    """

    def __init__(self) -> None:

        self.store = ChromaStore()


    # ==================================================
    # NORMALIZATION
    # ==================================================

    @staticmethod
    def _normalize_scope_value(
        value: str | None,
    ) -> str | None:
        """
        Convert application values into the normalized
        format used by the vector-store metadata.

        Example:

            Demo Municipal Corporation
                ->
            Demo_Municipal_Corporation

            District 3
                ->
            District_3

        Asset IDs are already normalized and therefore
        pass through the same function safely.
        """

        if value is None:
            return None

        normalized = (
            value
            .strip()
            .replace(" ", "_")
        )

        return normalized


    # ==================================================
    # SEARCH
    # ==================================================

    def search(
        self,
        query: str,
        client: str,
        district: str,
        asset: str | None = None,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Perform scoped semantic retrieval.

        Scope:

            client
            district
            optional asset

        Asset-aware ranking is applied after retrieval.
        """

        # --------------------------------------------------
        # Normalize application values
        # --------------------------------------------------

        normalized_client = (
            self._normalize_scope_value(
                client
            )
        )

        normalized_district = (
            self._normalize_scope_value(
                district
            )
        )

        normalized_asset = (
            self._normalize_scope_value(
                asset
            )
        )


        # --------------------------------------------------
        # Build metadata filters
        # --------------------------------------------------

        filters = {}

        if normalized_client:
            filters["client"] = (
                normalized_client
            )

        if normalized_district:
            filters["district"] = (
                normalized_district
            )


        # --------------------------------------------------
        # Perform semantic search
        # --------------------------------------------------

        results = self.store.search(
            query=query,
            top_k=top_k,
            filters=(
                filters
                if filters
                else None
            ),
        )


        # --------------------------------------------------
        # Asset-aware ranking
        # --------------------------------------------------

        for result in results:

            metadata = result.get(
                "metadata",
                {},
            )

            result_asset = metadata.get(
                "asset_id"
            )

            result["asset_match"] = (
                normalized_asset is not None
                and result_asset == normalized_asset
            )


        # --------------------------------------------------
        # Sort asset-specific evidence first
        # --------------------------------------------------

        results.sort(
            key=lambda item: (
                not item.get(
                    "asset_match",
                    False,
                ),
                item.get(
                    "distance",
                    float("inf"),
                ),
            )
        )


        return results