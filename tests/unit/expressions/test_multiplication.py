import pytest

import dice_roller


def test_init_empty():
    with pytest.raises(AssertionError):
        dice_roller.MultiplicationExpression(operands=[])


def test_roll():
    expression = dice_roller.MultiplicationExpression(
        operands=[
            dice_roller.ConstantExpression(value=1),
            dice_roller.ConstantExpression(value=2),
            dice_roller.ConstantExpression(value=3),
        ]
    )

    roll = expression.roll()

    assert roll == dice_roller.MultiplicationRollResult(
        result_items=[
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=1)),
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=2)),
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=3)),
        ]
    )


def test_get_histogram():
    expression = dice_roller.MultiplicationExpression(
        operands=[
            dice_roller.ConstantExpression(value=6),
            dice_roller.DiceExpression(sides=6),
        ]
    )

    histogram = expression.get_histogram()

    assert histogram == dice_roller.Histogram({6: 1, 12: 1, 18: 1, 24: 1, 30: 1, 36: 1})
