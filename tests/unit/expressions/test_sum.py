import pytest

import dice_roller


def test_init_empty():
    with pytest.raises(AssertionError):
        dice_roller.SumExpression(operands=[])


def test_roll():
    expression = dice_roller.SumExpression(
        operands=[
            dice_roller.ConstantExpression(value=1),
            dice_roller.ConstantExpression(value=2),
            dice_roller.ConstantExpression(value=3),
        ]
    )

    roll = expression.roll()

    assert roll == dice_roller.SumRollResult(
        result_items=[
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=1)),
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=2)),
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=3)),
        ]
    )


def test_get_histogram():
    expression = dice_roller.SumExpression(
        operands=[
            dice_roller.ConstantExpression(value=6),
            dice_roller.DiceExpression(sides=6),
        ]
    )

    histogram = expression.get_histogram()

    assert histogram == dice_roller.Histogram({7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1})
