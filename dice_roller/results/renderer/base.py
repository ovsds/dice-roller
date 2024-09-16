import abc
import typing

import dice_roller.results.models as result_models

_SingleRenderResultT = typing.TypeVar("_SingleRenderResultT")
_MultiRenderResultT = typing.TypeVar("_MultiRenderResultT")


class BaseResultRenderer(typing.Generic[_SingleRenderResultT, _MultiRenderResultT]):
    @abc.abstractmethod
    def render(self, roll: result_models.BaseResult) -> _MultiRenderResultT: ...

    def render_single(self, roll: result_models.BaseSingleResult) -> _SingleRenderResultT:
        if isinstance(roll, result_models.ValueResult):
            return self._render_value(roll)

        if isinstance(roll, result_models.SumResult):
            return self._render_sum(roll)

        if isinstance(roll, result_models.MultiplicationResult):
            return self._render_multiplication(roll)

        return self._unsupported(roll)  # pragma: no cover

    @abc.abstractmethod
    def _render_value(self, roll: result_models.ValueResult) -> _SingleRenderResultT: ...

    @abc.abstractmethod
    def _render_sum(self, roll: result_models.SumResult) -> _SingleRenderResultT: ...

    @abc.abstractmethod
    def _render_multiplication(self, roll: result_models.MultiplicationResult) -> _SingleRenderResultT: ...

    def _unsupported(self, roll: result_models.BaseResult) -> _SingleRenderResultT:
        raise NotImplementedError


__all__ = [
    "BaseResultRenderer",
]
