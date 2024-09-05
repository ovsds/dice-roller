class LexerError(Exception): ...


class UnknownTokenError(LexerError): ...


class ParseError(Exception): ...


class UnexpectedTokenError(ParseError): ...


class UnexpectedEndOfInputError(ParseError): ...


class UnexpectedStateError(ParseError): ...


__all__ = [
    "LexerError",
    "ParseError",
    "UnexpectedEndOfInputError",
    "UnexpectedTokenError",
    "UnknownTokenError",
]
