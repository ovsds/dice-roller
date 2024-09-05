import abc
import dataclasses
import typing

import dice_roller.results as results


@dataclasses.dataclass(frozen=True)
class BaseExpression(abc.ABC):
    @abc.abstractmethod
    def roll(self) -> results.BaseRollResult: ...


@dataclasses.dataclass(frozen=True)
class BaseOperationExpression(BaseExpression, abc.ABC):
    operands: typing.Sequence[BaseExpression]


__all__ = [
    "BaseExpression",
    "BaseOperationExpression",
]
