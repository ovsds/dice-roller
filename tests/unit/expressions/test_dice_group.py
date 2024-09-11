import pytest

import dice_roller


def test_init_invalid_count():
    with pytest.raises(AssertionError):
        dice_roller.DiceGroupExpression(
            count=0,
            dice=dice_roller.DiceExpression(sides=42),
        )


@pytest.mark.parametrize(
    "retain_lowest,retain_highest",
    [
        (-1, 0),
        (0, -1),
        (43, 0),
        (0, 43),
        (1, 1),
    ],
    ids=[
        "negative retain_lowest",
        "negative retain_highest",
        "retain_lowest > count",
        "retain_highest > count",
        "retain_lowest and retain_highest",
    ],
)
def test_init_invalid_drop_retain(
    retain_lowest: int,
    retain_highest: int,
):
    with pytest.raises(AssertionError):
        dice_roller.DiceGroupExpression(
            count=3,
            dice=dice_roller.DiceExpression(sides=42),
            retain_lowest=retain_lowest,
            retain_highest=retain_highest,
        )


def test_roll_default(fixed_random_seed: None):
    dice_group = dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=6),
        count=4,
    )

    roll = dice_group.roll()

    assert roll == dice_roller.SumRollResult(
        result_items=[
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=6)),
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=1)),
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=1)),
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=6)),
        ]
    )


def test_roll_retain_lowest(fixed_random_seed: None):
    dice_group = dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=6),
        count=4,
        retain_lowest=3,
    )

    roll = dice_group.roll()

    assert roll == dice_roller.SumRollResult(
        result_items=[
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=6), dropped=True),
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=1)),
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=1)),
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=6)),
        ]
    )


def test_roll_retain_highest(fixed_random_seed: None):
    dice_group = dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=6),
        count=4,
        retain_highest=3,
    )

    roll = dice_group.roll()

    assert roll == dice_roller.SumRollResult(
        result_items=[
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=6)),
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=1), dropped=True),
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=1)),
            dice_roller.RollResultItem(result=dice_roller.ValueRollResult(value=6)),
        ]
    )
