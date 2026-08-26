import re
from typing import Any


class CostEvidenceExtractor:
    """
    Extracts explicitly documented cost information
    from retrieved RAG evidence.

    IMPORTANT:

    This class does NOT estimate or invent values.

    It only extracts values that are explicitly present
    in the retrieved documents.
    """

    # ==================================================
    # UNIT RATE
    # ==================================================

    @staticmethod
    def extract_unit_rate(
        text: str,
    ) -> dict[str, Any] | None:
        """
        Extract a documented unit rate.

        Example supported text:

            Unit Rate:

            18.50 EUR / m²

        Returns:

            {
                "unit_rate": 18.50,
                "currency": "EUR",
                "unit": "m²"
            }
        """

        if not text:
            return None

        pattern = (
            r"Unit\s+Rate\s*:\s*"
            r"([0-9]+(?:\.[0-9]+)?)"
            r"\s*"
            r"([A-Za-z]+)"
            r"\s*/\s*"
            r"(m²|m2)"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if not match:
            return None

        unit_rate = float(
            match.group(1)
        )

        currency = (
            match.group(2)
            .upper()
        )

        unit = match.group(3)

        if unit == "m2":
            unit = "m²"

        return {
            "unit_rate": unit_rate,
            "currency": currency,
            "unit": unit,
        }


    # ==================================================
    # QUANTITY
    # ==================================================

    @staticmethod
    def extract_quantity(
        text: str,
    ) -> float | None:
        """
        Extract the explicitly documented
        estimated crossing marking area.

        Example:

            Estimated crossing marking area:

            24 m²
        """

        if not text:
            return None

        pattern = (
            r"Estimated\s+crossing\s+"
            r"marking\s+area\s*:\s*"
            r"([0-9]+(?:\.[0-9]+)?)"
            r"\s*(?:m²|m2)"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if not match:
            return None

        return float(
            match.group(1)
        )


    # ==================================================
    # EXTRACT FROM RESULTS
    # ==================================================

    @classmethod
    def extract_from_results(
        cls,
        results: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        """
        Search retrieved evidence for an explicit
        unit rate and quantity.

        Returns None unless BOTH are found.

        This prevents partial or invented calculations.
        """

        unit_rate_data = None

        quantity = None


        for result in results:

            text = result.get(
                "text",
                "",
            )


            # ------------------------------------------
            # Unit rate
            # ------------------------------------------

            if unit_rate_data is None:

                unit_rate_data = (
                    cls.extract_unit_rate(
                        text
                    )
                )


            # ------------------------------------------
            # Quantity
            # ------------------------------------------

            if quantity is None:

                quantity = (
                    cls.extract_quantity(
                        text
                    )
                )


            # ------------------------------------------
            # Stop when both are available
            # ------------------------------------------

            if (
                unit_rate_data is not None
                and quantity is not None
            ):
                break


        # ==================================================
        # BOTH ARE REQUIRED
        # ==================================================

        if (
            unit_rate_data is None
            or quantity is None
        ):
            return None


        return {
            "quantity": quantity,

            "unit": (
                unit_rate_data[
                    "unit"
                ]
            ),

            "unit_rate": (
                unit_rate_data[
                    "unit_rate"
                ]
            ),

            "currency": (
                unit_rate_data[
                    "currency"
                ]
            ),
        }