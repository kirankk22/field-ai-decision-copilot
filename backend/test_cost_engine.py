from app.cost.cost_engine import (
    CostEngine,
)


def main():

    print("=" * 80)
    print("PHASE 11.4 - DETERMINISTIC COST ENGINE")
    print("=" * 80)

    quantity = 24.0

    unit_rate = 18.50

    result = CostEngine.calculate(
        quantity=quantity,
        unit_rate=unit_rate,
        unit="m²",
        currency="EUR",
    )

    print()
    print("Quantity:")
    print(result.quantity)

    print()
    print("Unit:")
    print(result.unit)

    print()
    print("Unit Rate:")
    print(
        f"{result.unit_rate:.2f} "
        f"{result.currency}"
    )

    print()
    print("Total:")
    print(
        f"{result.total_cost:.2f} "
        f"{result.currency}"
    )

    print()
    print("-" * 80)

    expected = 444.00

    assert (
        result.total_cost ==
        expected
    )

    print(
        "COST TEST PASSED"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()