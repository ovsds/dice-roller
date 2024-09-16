import pytest

import dice_roller.parsers.expression as expression_parsers


def lexer_to_list(lexer: expression_parsers.ExpressionTextLexer) -> list[expression_parsers.ExpressionToken]:
    result: list[expression_parsers.ExpressionToken] = []
    while lexer.peek().type != expression_parsers.tokens.ExpressionTokenTypes.END_OF_INPUT:
        result.append(lexer.advance())

    return result


@pytest.mark.parametrize(
    "character",
    [" ", "\n", "\t", "\r"],
    ids=["space", "new_line", "tab", "carriage_return"],
)
def test_ignored_characters(character: str):
    lexer = expression_parsers.ExpressionTextLexer(text=f"4{character}2")

    assert lexer_to_list(lexer) == [
        expression_parsers.tokens.ExpressionToken(
            value="42",
            type=expression_parsers.tokens.ExpressionTokenTypes.NUMBER,
        )
    ]


@pytest.mark.parametrize(
    "value, token_type",
    [
        ("(", expression_parsers.tokens.ExpressionTokenTypes.LEFT_PARENTHESES),
        (")", expression_parsers.tokens.ExpressionTokenTypes.RIGHT_PARENTHESES),
        ("+", expression_parsers.tokens.ExpressionTokenTypes.PLUS),
        ("*", expression_parsers.tokens.ExpressionTokenTypes.MULTIPLY),
        ("x", expression_parsers.tokens.ExpressionTokenTypes.REPEAT),
    ],
    ids=["left_parentheses", "right_parentheses", "plus", "multiply", "repeat"],
)
def test_static_tokens(value: str, token_type: expression_parsers.tokens.ExpressionTokenTypes):
    lexer = expression_parsers.ExpressionTextLexer(text=f"4{value}2")

    assert lexer_to_list(lexer) == [
        expression_parsers.tokens.ExpressionToken(
            value="4",
            type=expression_parsers.tokens.ExpressionTokenTypes.NUMBER,
        ),
        expression_parsers.tokens.ExpressionToken(
            value=value,
            type=token_type,
        ),
        expression_parsers.tokens.ExpressionToken(
            value="2",
            type=expression_parsers.tokens.ExpressionTokenTypes.NUMBER,
        ),
    ]


def test_dice_group():
    lexer = expression_parsers.ExpressionTextLexer(text="4d6+abc")

    assert lexer_to_list(lexer) == [
        expression_parsers.tokens.ExpressionToken(
            value="4d6",
            type=expression_parsers.tokens.ExpressionTokenTypes.DICE_GROUP,
        ),
        expression_parsers.tokens.ExpressionToken(
            value="+",
            type=expression_parsers.tokens.ExpressionTokenTypes.PLUS,
        ),
        expression_parsers.tokens.ExpressionToken(
            value="abc",
            type=expression_parsers.tokens.ExpressionTokenTypes.DICE_GROUP,
        ),
    ]


def test_number():
    lexer = expression_parsers.ExpressionTextLexer(text="4+2")

    assert lexer_to_list(lexer) == [
        expression_parsers.tokens.ExpressionToken(
            value="4",
            type=expression_parsers.tokens.ExpressionTokenTypes.NUMBER,
        ),
        expression_parsers.tokens.ExpressionToken(
            value="+",
            type=expression_parsers.tokens.ExpressionTokenTypes.PLUS,
        ),
        expression_parsers.tokens.ExpressionToken(
            value="2",
            type=expression_parsers.tokens.ExpressionTokenTypes.NUMBER,
        ),
    ]
