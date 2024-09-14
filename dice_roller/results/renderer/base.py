import abc
import typing

import dice_roller.results.models as result_models

RenderResultT = typing.TypeVar("RenderResultT")


class BaseRollResultRenderer(typing.Generic[RenderResultT]):
    def render(self, roll: result_models.BaseRollResult) -> RenderResultT:
        if isinstance(roll, result_models.ValueRollResult):
            return self._render_value(roll)

        if isinstance(roll, result_models.SumRollResult):
            return self._render_sum(roll)

        if isinstance(roll, result_models.MultiplicationRollResult):
            return self._render_multiplication(roll)

        return self.unsupported(roll)  # pragma: no cover

    @abc.abstractmethod
    def _render_value(self, roll: result_models.ValueRollResult) -> RenderResultT: ...

    @abc.abstractmethod
    def _render_sum(self, roll: result_models.SumRollResult) -> RenderResultT: ...

    @abc.abstractmethod
    def _render_multiplication(self, roll: result_models.MultiplicationRollResult) -> RenderResultT: ...

    def unsupported(self, roll: result_models.BaseRollResult) -> RenderResultT:
        raise NotImplementedError


__all__ = [
    "BaseRollResultRenderer",
]
