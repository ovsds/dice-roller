import pytest

import dice_roller
import dice_roller.histograms as histograms
import dice_roller.results as results


def test_init_count_lt_1():
    with pytest.raises(AssertionError):
        dice_roller.RepeatedExpression(expression=dice_roller.ConstantExpression(value=1), count=0)


@pytest.mark.usefixtures("fixed_random_seed")
def test_roll():
    repeated = dice_roller.RepeatedExpression(expression=dice_roller.DiceExpression(sides=6), count=3)

    roll = repeated.roll()

    assert roll == results.MultiResult(
        results=[
            results.ValueResult(value=6),
            results.ValueResult(value=1),
            results.ValueResult(value=1),
        ]
    )


def test_get_histogram():
    repeated = dice_roller.RepeatedExpression(expression=dice_roller.DiceExpression(sides=6), count=3)

    histogram = repeated.get_histogram()

    assert histogram == histograms.Histogram(outcomes={1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1})
