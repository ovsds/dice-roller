import abc
import dataclasses
import typing

import typing_extensions

import dice_roller.results as results


class ExpressionProtocol(typing.Protocol):
    def roll(self) -> results.BaseRollResult: ...


class OperationExpressionProtocol(ExpressionProtocol, typing.Protocol):
    @classmethod
    def from_operands(cls, operands: typing.Sequence[ExpressionProtocol]) -> typing_extensions.Self: ...


@dataclasses.dataclass(frozen=True)
class BaseExpression(abc.ABC):
    @abc.abstractmethod
    def roll(self) -> results.BaseRollResult: ...


@dataclasses.dataclass(frozen=True)
class BaseOperationExpression(BaseExpression, abc.ABC):
    operands: typing.Sequence[ExpressionProtocol]

    @classmethod
    def from_operands(cls, operands: typing.Sequence[ExpressionProtocol]) -> typing_extensions.Self:
        return cls(operands=operands)


__all__ = [
    "BaseExpression",
    "BaseOperationExpression",
    "ExpressionProtocol",
    "OperationExpressionProtocol",
]
