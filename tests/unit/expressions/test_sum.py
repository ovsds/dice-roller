import pytest

import dice_roller
import dice_roller.histograms as histograms
import dice_roller.results as results


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

    assert roll == results.SumResult(
        result_items=[
            results.ResultItem(result=results.ValueResult(value=1)),
            results.ResultItem(result=results.ValueResult(value=2)),
            results.ResultItem(result=results.ValueResult(value=3)),
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

    assert histogram == histograms.Histogram({7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1})
