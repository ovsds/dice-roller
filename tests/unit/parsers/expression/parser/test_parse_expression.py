import dice_roller.expressions as expressions
import dice_roller.parsers.expression as expression_parsers


def test_default():
    expression = expression_parsers.parse_expression("(1d8+5)*(2d6+3)")
    assert expression == expressions.MultiplicationExpression(
        operands=[
            expressions.SumExpression(
                operands=[
                    expressions.DiceGroupExpression(count=1, dice=expressions.DiceExpression(sides=8)),
                    expressions.ConstantExpression(value=5),
                ]
            ),
            expressions.SumExpression(
                operands=[
                    expressions.DiceGroupExpression(count=2, dice=expressions.DiceExpression(sides=6)),
                    expressions.ConstantExpression(value=3),
                ]
            ),
        ],
    )
