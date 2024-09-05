import abc
import typing

import dice_roller.results.models as result_models

RenderResultT = typing.TypeVar("RenderResultT")


class BaseRollResultRenderer(typing.Generic[RenderResultT]):
    def render(self, roll: result_models.BaseRollResult) -> RenderResultT:
        if isinstance(roll, result_models.ValueRollResult):
            return self.render_value_roll(roll)

        if isinstance(roll, result_models.SumRollResult):
            return self.render_sum_roll(roll)

        if isinstance(roll, result_models.MultiplicationRollResult):
            return self.render_multiplication_roll(roll)

        return self.unsupported(roll)  # pragma: no cover

    @abc.abstractmethod
    def render_value_roll(self, roll: result_models.ValueRollResult) -> RenderResultT: ...

    @abc.abstractmethod
    def render_sum_roll(self, roll: result_models.SumRollResult) -> RenderResultT: ...

    @abc.abstractmethod
    def render_multiplication_roll(self, roll: result_models.MultiplicationRollResult) -> RenderResultT: ...

    def unsupported(self, roll: result_models.BaseRollResult) -> RenderResultT:
        raise NotImplementedError


__all__ = [
    "BaseRollResultRenderer",
]
