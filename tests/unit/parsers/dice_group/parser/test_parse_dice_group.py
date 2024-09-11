import dice_roller


def test_default():
    assert dice_roller.parse_dice_group("d8") == dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=8),
        count=1,
    )


def test_count():
    assert dice_roller.parse_dice_group("3d8") == dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=8),
        count=3,
    )


def test_constant():
    assert dice_roller.parse_dice_group("3") == dice_roller.ConstantExpression(value=3)


def test_retain_highest():
    assert dice_roller.parse_dice_group("3d8h2") == dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=8),
        count=3,
        retain_highest=2,
    )


def test_retain_lowest():
    assert dice_roller.parse_dice_group("3d8l2") == dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=8),
        count=3,
        retain_lowest=2,
    )
