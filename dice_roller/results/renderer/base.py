import abc
import typing

import dice_roller.results.models as result_models

RenderSingleResultT = typing.TypeVar("RenderSingleResultT")
RenderMultiResultT = typing.TypeVar("RenderMultiResultT")


class BaseRollResultRenderer(typing.Generic[RenderSingleResultT, RenderMultiResultT]):
    @abc.abstractmethod
    def render(self, roll: result_models.BaseRollResult) -> RenderMultiResultT: ...

    def render_single(self, roll: result_models.BaseSingleRollResult) -> RenderSingleResultT:
        if isinstance(roll, result_models.ValueRollResult):
            return self._render_value(roll)

        if isinstance(roll, result_models.SumRollResult):
            return self._render_sum(roll)

        if isinstance(roll, result_models.MultiplicationRollResult):
            return self._render_multiplication(roll)

        return self._unsupported(roll)  # pragma: no cover

    @abc.abstractmethod
    def _render_value(self, roll: result_models.ValueRollResult) -> RenderSingleResultT: ...

    @abc.abstractmethod
    def _render_sum(self, roll: result_models.SumRollResult) -> RenderSingleResultT: ...

    @abc.abstractmethod
    def _render_multiplication(self, roll: result_models.MultiplicationRollResult) -> RenderSingleResultT: ...

    def _unsupported(self, roll: result_models.BaseRollResult) -> RenderSingleResultT:
        raise NotImplementedError


__all__ = [
    "BaseRollResultRenderer",
]
