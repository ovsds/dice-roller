import dataclasses
import enum


class DiceGroupTokenTypes(enum.Enum):
    NUMBER = enum.auto()
    DICE_SPLITTER = enum.auto()
    RETAIN_LOWEST = enum.auto()
    RETAIN_HIGHEST = enum.auto()


@dataclasses.dataclass(frozen=True)
class DiceGroupToken:
    value: str
    type: DiceGroupTokenTypes


__all__ = [
    "DiceGroupToken",
    "DiceGroupTokenTypes",
]
