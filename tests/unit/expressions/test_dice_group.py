import pytest

import dice_roller
import dice_roller.histograms as histograms
import dice_roller.results as results


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


@pytest.mark.usefixtures("fixed_random_seed")
def test_roll_default():
    dice_group = dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=6),
        count=4,
    )

    roll = dice_group.roll()

    assert roll == results.SumRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=6)),
            results.RollResultItem(result=results.ValueRollResult(value=1)),
            results.RollResultItem(result=results.ValueRollResult(value=1)),
            results.RollResultItem(result=results.ValueRollResult(value=6)),
        ]
    )


@pytest.mark.usefixtures("fixed_random_seed")
def test_roll_retain_lowest():
    dice_group = dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=6),
        count=4,
        retain_lowest=3,
    )

    roll = dice_group.roll()

    assert roll == results.SumRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=6), dropped=True),
            results.RollResultItem(result=results.ValueRollResult(value=1)),
            results.RollResultItem(result=results.ValueRollResult(value=1)),
            results.RollResultItem(result=results.ValueRollResult(value=6)),
        ]
    )


@pytest.mark.usefixtures("fixed_random_seed")
def test_roll_retain_highest():
    dice_group = dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=6),
        count=4,
        retain_highest=3,
    )

    roll = dice_group.roll()

    assert roll == results.SumRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=6)),
            results.RollResultItem(result=results.ValueRollResult(value=1), dropped=True),
            results.RollResultItem(result=results.ValueRollResult(value=1)),
            results.RollResultItem(result=results.ValueRollResult(value=6)),
        ]
    )


def test_get_histogram_default():
    dice_group = dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=2),
        count=3,
    )

    histogram = dice_group.get_histogram()
    assert histogram == dice_group.get_histogram_greedily() == histograms.Histogram({3: 1, 4: 3, 5: 3, 6: 1})


def test_get_histogram_retain_lowest():
    dice_group = dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=2),
        count=3,
        retain_lowest=2,
    )

    histogram = dice_group.get_histogram()
    assert histogram == dice_group.get_histogram_greedily() == histograms.Histogram({2: 4, 3: 3, 4: 1})


def test_get_histogram_retain_highest():
    dice_group = dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=2),
        count=3,
        retain_highest=2,
    )

    histogram = dice_group.get_histogram()
    assert histogram == dice_group.get_histogram_greedily() == histograms.Histogram({2: 1, 3: 3, 4: 4})
