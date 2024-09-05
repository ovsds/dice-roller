import dataclasses

import dice_roller.expressions.base as dice_base
import dice_roller.results as results


@dataclasses.dataclass(frozen=True)
class ConstantExpression(dice_base.BaseExpression):
    value: int

    def roll(self) -> results.ValueRollResult:
        return results.ValueRollResult(self.value)


__all__ = [
    "ConstantExpression",
]
