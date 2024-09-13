import pytest

import dice_roller
import dice_roller.histograms as histograms
import dice_roller.results as results


def test_init_invalid_sides():
    with pytest.raises(AssertionError):
        dice_roller.DiceExpression(sides=0)


@pytest.mark.usefixtures("fixed_random_seed")
def test_roll():
    dice = dice_roller.DiceExpression(sides=20)
    roll = dice.roll()

    assert roll == results.ValueRollResult(value=4)


def test_get_histogram():
    dice = dice_roller.DiceExpression(sides=20)
    histogram = dice.get_histogram()

    assert histogram == histograms.Histogram({i: 1 for i in range(1, 21)})
