import dataclasses
import random

import dice_roller.results as results


@dataclasses.dataclass(frozen=True)
class DiceExpression:
    sides: int

    def __post_init__(self):
        assert self.sides > 0, "Number of sides must be positive"

    def roll(self) -> results.ValueRollResult:
        return results.ValueRollResult(value=random.randint(1, self.sides))


__all__ = [
    "DiceExpression",
]
