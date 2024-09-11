import pytest

import dice_roller.parsers.dice_group as dice_group_parsers
import dice_roller.parsers.exceptions as parser_exceptions


def test_default():
    lexer = dice_group_parsers.DiceGroupTextLexer(text="d8")

    assert list(lexer) == [
        dice_group_parsers.tokens.DiceGroupToken(
            value="d",
            type=dice_group_parsers.tokens.DiceGroupTokenTypes.DICE_SPLITTER,
        ),
        dice_group_parsers.tokens.DiceGroupToken(value="8", type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER),
    ]


def test_multiple_characters():
    lexer = dice_group_parsers.DiceGroupTextLexer(text="42d61h2l56")

    assert list(lexer) == [
        dice_group_parsers.tokens.DiceGroupToken(value="42", type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER),
        dice_group_parsers.tokens.DiceGroupToken(
            value="d",
            type=dice_group_parsers.tokens.DiceGroupTokenTypes.DICE_SPLITTER,
        ),
        dice_group_parsers.tokens.DiceGroupToken(value="61", type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER),
        dice_group_parsers.tokens.DiceGroupToken(
            value="h",
            type=dice_group_parsers.tokens.DiceGroupTokenTypes.RETAIN_HIGHEST,
        ),
        dice_group_parsers.tokens.DiceGroupToken(value="2", type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER),
        dice_group_parsers.tokens.DiceGroupToken(
            value="l",
            type=dice_group_parsers.tokens.DiceGroupTokenTypes.RETAIN_LOWEST,
        ),
        dice_group_parsers.tokens.DiceGroupToken(value="56", type=dice_group_parsers.tokens.DiceGroupTokenTypes.NUMBER),
    ]


def test_unexpected_token():
    lexer = dice_group_parsers.DiceGroupTextLexer(text="d8a")

    with pytest.raises(parser_exceptions.UnknownTokenError):
        list(lexer)
