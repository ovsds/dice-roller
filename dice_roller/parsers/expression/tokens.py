import dataclasses
import enum


class ExpressionTokenTypes(enum.Enum):
    END_OF_INPUT = enum.auto()
    LEFT_PARENTHESES = enum.auto()
    RIGHT_PARENTHESES = enum.auto()
    PLUS = enum.auto()
    MULTIPLY = enum.auto()
    DICE_GROUP = enum.auto()


@dataclasses.dataclass(frozen=True)
class ExpressionToken:
    value: str
    type: ExpressionTokenTypes


__all__ = [
    "ExpressionToken",
    "ExpressionTokenTypes",
]
