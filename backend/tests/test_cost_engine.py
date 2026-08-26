from app.cost.cost_engine import CostEngine


def test_cost_calculation():
    """
    Verify deterministic cost calculation.
    """

    result = CostEngine.calculate(
        quantity=24.0,
        unit_rate=18.50,
        unit="m²",
        currency="EUR",
    )

    assert result.quantity == 24.0
    assert result.unit == "m²"
    assert result.unit_rate == 18.50
    assert result.currency == "EUR"
    assert result.total_cost == 444.0


def test_cost_calculation_zero_quantity():
    """
    Verify that zero quantity produces zero cost.
    """

    result = CostEngine.calculate(
        quantity=0.0,
        unit_rate=18.50,
        unit="m²",
        currency="EUR",
    )

    assert result.total_cost == 0.0