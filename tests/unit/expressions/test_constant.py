import dice_roller


def test_roll():
    dice = dice_roller.ConstantExpression(value=3)
    assert dice.roll() == dice_roller.ValueRollResult(value=3)


def test_get_histogram():
    dice = dice_roller.ConstantExpression(value=3)
    assert dice.get_histogram() == dice_roller.Histogram({3: 1})
