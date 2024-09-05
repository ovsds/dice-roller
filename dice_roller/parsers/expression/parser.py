import dataclasses
import typing

import dice_roller.expressions as expressions
import dice_roller.parsers.dice_group as dice_group_parsers
import dice_roller.parsers.exceptions as exceptions
import dice_roller.parsers.expression.lexers as lexers
import dice_roller.parsers.expression.tokens as tokens


@dataclasses.dataclass(frozen=True)
class OperatorParseOptions:
    expression_class: type[expressions.BaseOperationExpression]
    lesser_precedence_operators: list[tokens.ExpressionTokenTypes] = dataclasses.field(default_factory=list)


OPERATOR_TOKENS_MAP: typing.Mapping[tokens.ExpressionTokenTypes, OperatorParseOptions] = {
    tokens.ExpressionTokenTypes.PLUS: OperatorParseOptions(
        expression_class=expressions.SumExpression,
    ),
    tokens.ExpressionTokenTypes.MULTIPLY: OperatorParseOptions(
        expression_class=expressions.MultiplicationExpression,
        lesser_precedence_operators=[tokens.ExpressionTokenTypes.PLUS],
    ),
}


@dataclasses.dataclass(frozen=True)
class State:
    operands: list[expressions.BaseExpression] = dataclasses.field(default_factory=list)
    operator: tokens.ExpressionTokenTypes | None = None

    def resolve(self) -> expressions.BaseExpression:
        if len(self.operands) == 0:
            raise exceptions.UnexpectedEndOfInputError

        if len(self.operands) == 1:
            assert self.operator is None
            return self.operands[0]

        if self.operator is None:
            raise exceptions.UnexpectedStateError("Missing operator token")  # pragma: no cover

        return OPERATOR_TOKENS_MAP[self.operator].expression_class(operands=self.operands)


class ExpressionParser:
    def __init__(self, lexer: lexers.ExpressionLexerProtocol):
        self.lexer = lexer

    def parse(self) -> expressions.BaseExpression:
        return self._parse(end_tokens_types=[tokens.ExpressionTokenTypes.END_OF_INPUT])

    def _parse(
        self,
        end_tokens_types: list[tokens.ExpressionTokenTypes],
    ) -> expressions.BaseExpression:
        state = State()

        while self.lexer.peek().type not in end_tokens_types:
            current_token = self.lexer.peek()

            if current_token.type in OPERATOR_TOKENS_MAP:
                state = self._parse_operator(state, end_tokens_types)
            elif current_token.type == tokens.ExpressionTokenTypes.LEFT_PARENTHESES:
                state = self._parse_parentheses(state)
            elif current_token.type == tokens.ExpressionTokenTypes.DICE_GROUP:
                state = self._parse_dice_group(state)

        return state.resolve()

    def _parse_operator(self, state: State, end_tokens_types: list[tokens.ExpressionTokenTypes]) -> State:
        if len(state.operands) == 0:
            raise exceptions.UnexpectedTokenError("Unexpected operator token")

        current_token = self.lexer.peek()

        if (
            state.operator is not None
            and current_token.type in OPERATOR_TOKENS_MAP[state.operator].lesser_precedence_operators
        ):
            return State(
                operator=current_token.type,
                operands=[state.resolve()],
            )

        operator = state.operator or current_token.type
        if current_token.type == operator:
            self.lexer.advance()

            extended_end_tokens_types = end_tokens_types.copy()
            extended_end_tokens_types.append(operator)
            extended_end_tokens_types.extend(OPERATOR_TOKENS_MAP[operator].lesser_precedence_operators)
            operands = state.operands.copy()
            operands.append(self._parse(end_tokens_types=extended_end_tokens_types))

            return State(operator=operator, operands=operands)

        raise exceptions.UnexpectedStateError("Invalid operator precedence")  # pragma: no cover

    def _parse_parentheses(self, state: State) -> State:
        token = self.lexer.advance()
        assert token.type == tokens.ExpressionTokenTypes.LEFT_PARENTHESES

        operand = self._parse(end_tokens_types=[tokens.ExpressionTokenTypes.RIGHT_PARENTHESES])

        token = self.lexer.advance()
        assert token.type == tokens.ExpressionTokenTypes.RIGHT_PARENTHESES

        operands = state.operands.copy()
        operands.append(operand)

        return State(operator=state.operator, operands=operands)

    def _parse_dice_group(self, state: State) -> State:
        if len(state.operands) > 0:
            raise exceptions.UnexpectedTokenError("Unexpected dice group token")

        if state.operator is not None:
            raise exceptions.UnexpectedStateError("Operator is not None when parsing dice group")  # pragma: no cover

        token = self.lexer.advance()
        assert token.type == tokens.ExpressionTokenTypes.DICE_GROUP

        lexer = dice_group_parsers.DiceGroupTextLexer(text=token.value)
        parser = dice_group_parsers.DiceGroupParser(lexer=lexer)
        operand = parser.parse()

        return State(operands=[operand])


def parse_expression(text: str) -> expressions.BaseExpression:
    lexer = lexers.ExpressionTextLexer(text=text)
    parser = ExpressionParser(lexer=lexer)

    return parser.parse()


__all__ = [
    "ExpressionParser",
    "parse_expression",
]
