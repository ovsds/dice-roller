import dataclasses

import dice_roller.results as results


@dataclasses.dataclass(frozen=True)
class ConstantExpression:
    value: int

    def roll(self) -> results.ValueRollResult:
        return results.ValueRollResult(self.value)


__all__ = [
    "ConstantExpression",
]
