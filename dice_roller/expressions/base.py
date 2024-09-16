import abc
import dataclasses
import typing

import typing_extensions

import dice_roller.histograms as histograms
import dice_roller.results as results


class ExpressionProtocol(typing.Protocol):
    def roll(self) -> results.BaseResult: ...

    def get_histogram(self) -> histograms.Histogram: ...


class SingleExpressionProtocol(ExpressionProtocol, typing.Protocol):
    def roll(self) -> results.BaseSingleResult: ...


class OperationExpressionProtocol(SingleExpressionProtocol, typing.Protocol):
    @classmethod
    def from_operands(cls, operands: typing.Sequence[SingleExpressionProtocol]) -> typing_extensions.Self: ...


@dataclasses.dataclass(frozen=True)
class BaseExpression(abc.ABC): ...


@dataclasses.dataclass(frozen=True)
class BaseOperationExpression(BaseExpression, abc.ABC):
    operands: typing.Sequence[SingleExpressionProtocol]

    @classmethod
    def from_operands(cls, operands: typing.Sequence[SingleExpressionProtocol]) -> typing_extensions.Self:
        return cls(operands=operands)


__all__ = [
    "BaseExpression",
    "BaseOperationExpression",
    "ExpressionProtocol",
    "OperationExpressionProtocol",
    "SingleExpressionProtocol",
]
