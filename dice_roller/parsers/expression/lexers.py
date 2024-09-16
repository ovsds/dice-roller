import typing

import dice_roller.parsers.expression.tokens as tokens


class ExpressionLexerProtocol(typing.Protocol):
    def peek(self) -> tokens.ExpressionToken: ...

    def advance(self) -> tokens.ExpressionToken: ...


class ExpressionTextLexer:
    IGNORED_CHARACTERS = {
        " ",
        "\n",
        "\t",
        "\r",
    }

    STATIC_TOKENS_MAP = {
        "(": tokens.ExpressionTokenTypes.LEFT_PARENTHESES,
        ")": tokens.ExpressionTokenTypes.RIGHT_PARENTHESES,
        "+": tokens.ExpressionTokenTypes.PLUS,
        "*": tokens.ExpressionTokenTypes.MULTIPLY,
        "x": tokens.ExpressionTokenTypes.REPEAT,
    }

    def __init__(self, text: str):
        self.text = text
        self.index = 0
        self._next_token: tokens.ExpressionToken | None = None

    def peek(self) -> tokens.ExpressionToken:
        if self._next_token is None:
            self._next_token = self.advance()

        return self._next_token

    def advance(self) -> tokens.ExpressionToken:
        if self._next_token is None:
            return self._get_next()

        next_token = self._next_token
        self._next_token = None
        return next_token

    def _get_token_from_chars(self, chars: list[str]) -> tokens.ExpressionToken:
        value = "".join(chars)
        if value.isdigit():
            return tokens.ExpressionToken(value=value, type=tokens.ExpressionTokenTypes.NUMBER)

        return tokens.ExpressionToken(value=value, type=tokens.ExpressionTokenTypes.DICE_GROUP)

    def _get_next(self) -> tokens.ExpressionToken:
        current_token_chars: list[str] = []

        while self.index < len(self.text):
            current_char = self.text[self.index]

            if current_char in self.IGNORED_CHARACTERS:
                self.index += 1
                continue

            if current_char not in self.STATIC_TOKENS_MAP:
                current_token_chars.append(current_char)
                self.index += 1
                continue

            if current_token_chars:
                return self._get_token_from_chars(current_token_chars)

            self.index += 1
            return tokens.ExpressionToken(value=current_char, type=self.STATIC_TOKENS_MAP[current_char])

        if current_token_chars:
            return self._get_token_from_chars(current_token_chars)

        return tokens.ExpressionToken(value="", type=tokens.ExpressionTokenTypes.END_OF_INPUT)


__all__ = [
    "ExpressionLexerProtocol",
    "ExpressionTextLexer",
]
