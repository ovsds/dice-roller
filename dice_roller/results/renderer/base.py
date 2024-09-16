import abc
import typing

import dice_roller.results.models as result_models

_CT = typing.TypeVar("_CT", covariant=True)


class ResultRendererProtocol(typing.Protocol[_CT]):
    def render(self, roll: result_models.BaseResult) -> _CT: ...


class BaseListResultRenderer(typing.Generic[_CT], abc.ABC):
    def render(self, roll: result_models.BaseResult) -> list[_CT]:
        if isinstance(roll, result_models.MultiResult):
            return [self._render_single(item) for item in roll.results]

        if isinstance(roll, result_models.BaseSingleResult):
            return [self._render_single(roll)]

        return [self._unsupported(roll)]  # pragma: no cover

    def _render_single(self, roll: result_models.BaseSingleResult) -> _CT:
        if isinstance(roll, result_models.ValueResult):
            return self._render_value(roll)

        if isinstance(roll, result_models.SumResult):
            return self._render_sum(roll)

        if isinstance(roll, result_models.MultiplicationResult):
            return self._render_multiplication(roll)

        return self._unsupported(roll)  # pragma: no cover

    @abc.abstractmethod
    def _render_value(self, roll: result_models.ValueResult) -> _CT: ...

    @abc.abstractmethod
    def _render_sum(self, roll: result_models.SumResult) -> _CT: ...

    @abc.abstractmethod
    def _render_multiplication(self, roll: result_models.MultiplicationResult) -> _CT: ...

    def _unsupported(self, roll: result_models.BaseResult) -> _CT:
        raise ValueError(f"Unsupported roll type: {type(roll)}")  # pragma: no cover


__all__ = [
    "BaseListResultRenderer",
    "ResultRendererProtocol",
]
