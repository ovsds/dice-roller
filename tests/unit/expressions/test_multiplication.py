import pytest

import dice_roller
import dice_roller.histograms as histograms
import dice_roller.results as results


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

    assert roll == results.MultiplicationRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=1)),
            results.RollResultItem(result=results.ValueRollResult(value=2)),
            results.RollResultItem(result=results.ValueRollResult(value=3)),
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

    assert histogram == histograms.Histogram({6: 1, 12: 1, 18: 1, 24: 1, 30: 1, 36: 1})
