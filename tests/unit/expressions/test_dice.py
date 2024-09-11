import pytest

import dice_roller


def test_init_invalid_sides():
    with pytest.raises(AssertionError):
        dice_roller.DiceExpression(sides=0)


def test_roll(fixed_random_seed: None):
    dice = dice_roller.DiceExpression(sides=20)
    roll = dice.roll()

    assert roll == dice_roller.ValueRollResult(value=4)
