import dice_roller.expressions as expressions
import dice_roller.parsers.dice_group.lexers as lexers
import dice_roller.parsers.dice_group.tokens as tokens
import dice_roller.parsers.exceptions as parser_exceptions

DEFAULT_DICE_GROUP_COUNT = 1
DEFAULT_DICE_GROUP_RETAIN_HIGHEST = 0
DEFAULT_DICE_GROUP_RETAIN_LOWEST = 0


class DiceGroupParser:
    def __init__(self, lexer: lexers.DiceGroupLexerProtocol):
        self.lexer = lexer
        self._current_token: tokens.DiceGroupToken | None = None

    def _advance(self):
        self._current_token = next(self.lexer, None)

    def _parse_number(self) -> int:
        if self._current_token is None:
            raise parser_exceptions.UnexpectedEndOfInputError

        if self._current_token.type != tokens.DiceGroupTokenTypes.NUMBER:
            raise parser_exceptions.UnexpectedTokenError("Unexpected token type, expected number")

        value = int(self._current_token.value)
        self._advance()
        return value

    def _parse_optional_number(self) -> int | None:
        if self._current_token is None:
            return None

        if self._current_token.type != tokens.DiceGroupTokenTypes.NUMBER:
            return None

        value = int(self._current_token.value)
        self._advance()
        return value

    def _skip_optional_token(self, token_type: tokens.DiceGroupTokenTypes) -> bool:
        if self._current_token is None:
            return False

        if self._current_token.type != token_type:
            return False

        self._advance()
        return True

    def parse(self) -> expressions.SingleExpressionProtocol:
        self._advance()

        count = self._parse_optional_number()
        dice_splitter = self._skip_optional_token(tokens.DiceGroupTokenTypes.DICE_SPLITTER)
        if not dice_splitter:
            if self._current_token is not None:
                raise parser_exceptions.UnexpectedTokenError

            if count is None:
                raise parser_exceptions.UnexpectedEndOfInputError

            return expressions.ConstantExpression(value=count)

        count = count or DEFAULT_DICE_GROUP_COUNT
        dice_sides = self._parse_number()

        retain_highest = DEFAULT_DICE_GROUP_RETAIN_HIGHEST
        retain_lowest = DEFAULT_DICE_GROUP_RETAIN_LOWEST

        while self._current_token is not None:
            if self._skip_optional_token(tokens.DiceGroupTokenTypes.RETAIN_LOWEST):
                retain_lowest = self._parse_number()
            elif self._skip_optional_token(tokens.DiceGroupTokenTypes.RETAIN_HIGHEST):
                retain_highest = self._parse_number()
            else:
                raise parser_exceptions.UnexpectedTokenError

        return expressions.DiceGroupExpression(
            count=count,
            dice=expressions.DiceExpression(
                sides=dice_sides,
            ),
            retain_highest=retain_highest,
            retain_lowest=retain_lowest,
        )


def parse_dice_group(text: str) -> expressions.SingleExpressionProtocol:
    lexer = lexers.DiceGroupTextLexer(text=text)
    parser = DiceGroupParser(lexer=lexer)

    return parser.parse()


__all__ = [
    "DiceGroupParser",
    "parse_dice_group",
]
