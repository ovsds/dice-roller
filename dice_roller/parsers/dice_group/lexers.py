import typing

import dice_roller.parsers.dice_group.tokens as tokens
import dice_roller.parsers.exceptions as parser_exceptions


class DiceGroupLexerProtocol(typing.Protocol):
    def __next__(self) -> tokens.DiceGroupToken: ...


class DiceGroupTextLexer:
    STATIC_TOKENS = {
        "d": tokens.DiceGroupTokenTypes.DICE_SPLITTER,
        "l": tokens.DiceGroupTokenTypes.RETAIN_LOWEST,
        "h": tokens.DiceGroupTokenTypes.RETAIN_HIGHEST,
    }

    def __init__(self, text: str):
        self.text = text
        self.index = 0

    def __iter__(self):
        return self

    def _check_static_token_at_index(self, index: int) -> str | None:
        for token in self.STATIC_TOKENS.keys():
            if self.text[index : index + len(token)] == token:
                return token

        return None

    def __next__(self) -> tokens.DiceGroupToken:
        token_start_index = self.index

        while self.index < len(self.text):
            static_token = self._check_static_token_at_index(self.index)

            if static_token is not None:
                if token_start_index != self.index:
                    break

                self.index += len(static_token)
                return tokens.DiceGroupToken(value=static_token, type=self.STATIC_TOKENS[static_token])

            self.index += 1

        if token_start_index == self.index:
            raise StopIteration

        token = self.text[token_start_index : self.index]

        if not token.isdigit():
            raise parser_exceptions.UnknownTokenError(f"Unknown token: {token}")

        return tokens.DiceGroupToken(value=token, type=tokens.DiceGroupTokenTypes.NUMBER)


__all__ = [
    "DiceGroupLexerProtocol",
    "DiceGroupTextLexer",
]
