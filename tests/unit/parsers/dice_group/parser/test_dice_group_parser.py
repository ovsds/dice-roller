import pytest

import dice_roller
import dice_roller.parsers.dice_group as dice_group_parsers
import dice_roller.parsers.exceptions as parser_exceptions


def test_default():
    lexer = iter(
        [
            dice_group_parsers.tokens.DiceGroupToken(
                value="d",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.DICE_SPLITTER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="8", type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER
            ),
        ]
    )
    parser = dice_group_parsers.DiceGroupParser(lexer=lexer)

    expression = parser.parse()

    assert expression == dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=8),
        count=1,
    )


def test_count():
    lexer = iter(
        [
            dice_group_parsers.tokens.DiceGroupToken(
                value="3",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="d",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.DICE_SPLITTER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="8",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
        ]
    )
    parser = dice_group_parsers.DiceGroupParser(lexer=lexer)

    expression = parser.parse()

    assert expression == dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=8),
        count=3,
    )


def test_constant():
    lexer = iter(
        [
            dice_group_parsers.tokens.DiceGroupToken(
                value="3",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
        ]
    )
    parser = dice_group_parsers.DiceGroupParser(lexer=lexer)

    expression = parser.parse()

    assert expression == dice_roller.ConstantExpression(value=3)


def test_empty_raises():
    lexer = iter([])
    parser = dice_group_parsers.DiceGroupParser(lexer=lexer)

    with pytest.raises(parser_exceptions.UnexpectedEndOfInputError):
        parser.parse()


def test_unexpected_starting_token_raises():
    lexer = iter(
        [
            dice_group_parsers.tokens.DiceGroupToken(
                value="l",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.RETAIN_LOWEST,
            ),
        ]
    )
    parser = dice_group_parsers.DiceGroupParser(lexer=lexer)

    with pytest.raises(parser_exceptions.UnexpectedTokenError):
        parser.parse()


def test_without_sides_raises():
    lexer = iter(
        [
            dice_group_parsers.tokens.DiceGroupToken(
                value="3",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="d",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.DICE_SPLITTER,
            ),
        ]
    )
    parser = dice_group_parsers.DiceGroupParser(lexer=lexer)

    with pytest.raises(parser_exceptions.UnexpectedEndOfInputError):
        parser.parse()


def test_without_sides_with_drop_raises():
    lexer = iter(
        [
            dice_group_parsers.tokens.DiceGroupToken(
                value="3",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="d",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.DICE_SPLITTER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="l",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.RETAIN_LOWEST,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="1",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
        ]
    )
    parser = dice_group_parsers.DiceGroupParser(lexer=lexer)

    with pytest.raises(parser_exceptions.UnexpectedTokenError):
        parser.parse()


def test_retain_lowest():
    lexer = iter(
        [
            dice_group_parsers.tokens.DiceGroupToken(
                value="4",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="d",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.DICE_SPLITTER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="6",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="l",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.RETAIN_LOWEST,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="1",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
        ]
    )
    parser = dice_group_parsers.DiceGroupParser(lexer=lexer)

    expression = parser.parse()

    assert expression == dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=6),
        count=4,
        retain_lowest=1,
    )


def test_retain_highest():
    lexer = iter(
        [
            dice_group_parsers.tokens.DiceGroupToken(
                value="4",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="d",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.DICE_SPLITTER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="6",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="h",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.RETAIN_HIGHEST,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="1",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
        ]
    )
    parser = dice_group_parsers.DiceGroupParser(lexer=lexer)

    expression = parser.parse()

    assert expression == dice_roller.DiceGroupExpression(
        dice=dice_roller.DiceExpression(sides=6),
        count=4,
        retain_highest=1,
    )


def test_multiple_dice_splitters_raises():
    lexer = iter(
        [
            dice_group_parsers.tokens.DiceGroupToken(
                value="4",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="d",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.DICE_SPLITTER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="6",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="d",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.DICE_SPLITTER,
            ),
            dice_group_parsers.tokens.DiceGroupToken(
                value="6",
                type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER,
            ),
        ]
    )
    parser = dice_group_parsers.DiceGroupParser(lexer=lexer)

    with pytest.raises(parser_exceptions.UnexpectedTokenError):
        parser.parse()
