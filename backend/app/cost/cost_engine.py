from dataclasses import dataclass


@dataclass
class CostCalculation:
    """
    Deterministic cost calculation result.
    """

    quantity: float
    unit: str
    unit_rate: float
    currency: str
    total_cost: float


class CostEngine:
    """
    Performs deterministic cost calculations.

    The LLM must never perform these calculations itself.
    """

    @staticmethod
    def calculate(
        quantity: float,
        unit_rate: float,
        unit: str,
        currency: str,
    ) -> CostCalculation:

        if quantity < 0:
            raise ValueError(
                "Quantity cannot be negative."
            )

        if unit_rate < 0:
            raise ValueError(
                "Unit rate cannot be negative."
            )

        total_cost = (
            quantity *
            unit_rate
        )

        return CostCalculation(
            quantity=quantity,
            unit=unit,
            unit_rate=unit_rate,
            currency=currency,
            total_cost=round(
                total_cost,
                2,
            ),
        )