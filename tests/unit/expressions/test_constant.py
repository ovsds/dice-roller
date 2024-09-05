import dice_roller


def test_roll():
    dice = dice_roller.ConstantExpression(value=3)
    assert dice.roll() == dice_roller.ValueRollResult(value=3)
