import pytest

import dice_roller
import dice_roller.parsers.exceptions as parsers_exceptions
import dice_roller.parsers.expression as expression_parsers


class ExpressionListLexer:
    def __init__(self, tokens_list: list[expression_parsers.ExpressionToken]):
        self.tokens_list = tokens_list
        self.index = 0

    def peek(self) -> expression_parsers.ExpressionToken:
        if self.index >= len(self.tokens_list):
            return expression_parsers.ExpressionToken(
                value="",
                type=expression_parsers.ExpressionTokenTypes.END_OF_INPUT,
            )

        return self.tokens_list[self.index]

    def advance(self) -> expression_parsers.ExpressionToken:
        if self.index >= len(self.tokens_list):
            return expression_parsers.ExpressionToken(
                value="",
                type=expression_parsers.ExpressionTokenTypes.END_OF_INPUT,
            )

        token = self.tokens_list[self.index]
        self.index += 1
        return token


def test_dice_group():
    lexer = ExpressionListLexer(
        tokens_list=[
            expression_parsers.ExpressionToken(
                value="1d8",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
        ]
    )
    parser = expression_parsers.ExpressionParser(lexer=lexer)

    expression = parser.parse()
    assert expression == dice_roller.DiceGroupExpression(
        count=1,
        dice=dice_roller.DiceExpression(sides=8),
    )


def test_dice_group_parentheses():
    lexer = ExpressionListLexer(
        tokens_list=[
            expression_parsers.ExpressionToken(
                value="(",
                type=expression_parsers.ExpressionTokenTypes.LEFT_PARENTHESES,
            ),
            expression_parsers.ExpressionToken(
                value="1d8",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
            expression_parsers.ExpressionToken(
                value=")",
                type=expression_parsers.ExpressionTokenTypes.RIGHT_PARENTHESES,
            ),
        ]
    )
    parser = expression_parsers.ExpressionParser(lexer=lexer)

    expression = parser.parse()
    assert expression == dice_roller.DiceGroupExpression(
        count=1,
        dice=dice_roller.DiceExpression(sides=8),
    )


def test_nested_parentheses():
    lexer = ExpressionListLexer(
        tokens_list=[
            expression_parsers.ExpressionToken(
                value="(",
                type=expression_parsers.ExpressionTokenTypes.LEFT_PARENTHESES,
            ),
            expression_parsers.ExpressionToken(
                value="(",
                type=expression_parsers.ExpressionTokenTypes.LEFT_PARENTHESES,
            ),
            expression_parsers.ExpressionToken(
                value="1d8",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
            expression_parsers.ExpressionToken(
                value=")",
                type=expression_parsers.ExpressionTokenTypes.RIGHT_PARENTHESES,
            ),
            expression_parsers.ExpressionToken(
                value=")",
                type=expression_parsers.ExpressionTokenTypes.RIGHT_PARENTHESES,
            ),
        ]
    )
    parser = expression_parsers.ExpressionParser(lexer=lexer)

    expression = parser.parse()
    assert expression == dice_roller.DiceGroupExpression(
        count=1,
        dice=dice_roller.DiceExpression(sides=8),
    )


def test_sum_expression():
    lexer = ExpressionListLexer(
        tokens_list=[
            expression_parsers.ExpressionToken(
                value="1d8",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
            expression_parsers.ExpressionToken(
                value="+",
                type=expression_parsers.ExpressionTokenTypes.PLUS,
            ),
            expression_parsers.ExpressionToken(
                value="2d6",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
            expression_parsers.ExpressionToken(
                value="+",
                type=expression_parsers.ExpressionTokenTypes.PLUS,
            ),
            expression_parsers.ExpressionToken(
                value="3",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
        ]
    )
    parser = expression_parsers.ExpressionParser(lexer=lexer)

    expression = parser.parse()
    assert expression == dice_roller.SumExpression(
        operands=[
            dice_roller.DiceGroupExpression(count=1, dice=dice_roller.DiceExpression(sides=8)),
            dice_roller.DiceGroupExpression(count=2, dice=dice_roller.DiceExpression(sides=6)),
            dice_roller.ConstantExpression(value=3),
        ],
    )


def test_multiplication_expression():
    lexer = ExpressionListLexer(
        tokens_list=[
            expression_parsers.ExpressionToken(
                value="1d8",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
            expression_parsers.ExpressionToken(
                value="*",
                type=expression_parsers.ExpressionTokenTypes.MULTIPLY,
            ),
            expression_parsers.ExpressionToken(
                value="2d6",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
            expression_parsers.ExpressionToken(
                value="*",
                type=expression_parsers.ExpressionTokenTypes.MULTIPLY,
            ),
            expression_parsers.ExpressionToken(
                value="3",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
        ]
    )
    parser = expression_parsers.ExpressionParser(lexer=lexer)

    expression = parser.parse()
    assert expression == dice_roller.MultiplicationExpression(
        operands=[
            dice_roller.DiceGroupExpression(count=1, dice=dice_roller.DiceExpression(sides=8)),
            dice_roller.DiceGroupExpression(count=2, dice=dice_roller.DiceExpression(sides=6)),
            dice_roller.ConstantExpression(value=3),
        ],
    )


def test_sum_and_multiplication_expression():
    lexer = ExpressionListLexer(
        tokens_list=[
            expression_parsers.ExpressionToken(
                value="1d8",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
            expression_parsers.ExpressionToken(
                value="+",
                type=expression_parsers.ExpressionTokenTypes.PLUS,
            ),
            expression_parsers.ExpressionToken(
                value="2d6",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
            expression_parsers.ExpressionToken(
                value="*",
                type=expression_parsers.ExpressionTokenTypes.MULTIPLY,
            ),
            expression_parsers.ExpressionToken(
                value="3",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
        ]
    )
    parser = expression_parsers.ExpressionParser(lexer=lexer)

    expression = parser.parse()
    assert expression == dice_roller.SumExpression(
        operands=[
            dice_roller.DiceGroupExpression(count=1, dice=dice_roller.DiceExpression(sides=8)),
            dice_roller.MultiplicationExpression(
                operands=[
                    dice_roller.DiceGroupExpression(count=2, dice=dice_roller.DiceExpression(sides=6)),
                    dice_roller.ConstantExpression(value=3),
                ],
            ),
        ],
    )


def test_multiplication_and_sum_expression():
    lexer = ExpressionListLexer(
        tokens_list=[
            expression_parsers.ExpressionToken(
                value="1d8",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
            expression_parsers.ExpressionToken(
                value="*",
                type=expression_parsers.ExpressionTokenTypes.MULTIPLY,
            ),
            expression_parsers.ExpressionToken(
                value="2d6",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
            expression_parsers.ExpressionToken(
                value="+",
                type=expression_parsers.ExpressionTokenTypes.PLUS,
            ),
            expression_parsers.ExpressionToken(
                value="3",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
        ]
    )
    parser = expression_parsers.ExpressionParser(lexer=lexer)

    expression = parser.parse()
    assert expression == dice_roller.SumExpression(
        operands=[
            dice_roller.MultiplicationExpression(
                operands=[
                    dice_roller.DiceGroupExpression(count=1, dice=dice_roller.DiceExpression(sides=8)),
                    dice_roller.DiceGroupExpression(count=2, dice=dice_roller.DiceExpression(sides=6)),
                ],
            ),
            dice_roller.ConstantExpression(value=3),
        ],
    )


def test_unexpected_operator():
    lexer = ExpressionListLexer(
        tokens_list=[
            expression_parsers.ExpressionToken(
                value="+",
                type=expression_parsers.ExpressionTokenTypes.PLUS,
            ),
        ]
    )
    parser = expression_parsers.ExpressionParser(lexer=lexer)

    with pytest.raises(parsers_exceptions.UnexpectedTokenError):
        parser.parse()


def test_unexpected_empty_expression():
    lexer = ExpressionListLexer(
        tokens_list=[
            expression_parsers.ExpressionToken(
                value="(",
                type=expression_parsers.ExpressionTokenTypes.LEFT_PARENTHESES,
            ),
            expression_parsers.ExpressionToken(
                value=")",
                type=expression_parsers.ExpressionTokenTypes.RIGHT_PARENTHESES,
            ),
        ]
    )
    parser = expression_parsers.ExpressionParser(lexer=lexer)

    with pytest.raises(parsers_exceptions.UnexpectedEndOfInputError):
        parser.parse()


def test_unexpected_dice_group():
    lexer = ExpressionListLexer(
        tokens_list=[
            expression_parsers.ExpressionToken(
                value="1d8",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
            expression_parsers.ExpressionToken(
                value="1d8",
                type=expression_parsers.ExpressionTokenTypes.DICE_GROUP,
            ),
        ]
    )
    parser = expression_parsers.ExpressionParser(lexer=lexer)

    with pytest.raises(parsers_exceptions.UnexpectedTokenError):
        parser.parse()
