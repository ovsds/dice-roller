import dataclasses

import dice_roller.expressions.base as dice_base
import dice_roller.results as results


@dataclasses.dataclass(frozen=True)
class MultiplicationExpression(dice_base.BaseOperationExpression):
    def __post_init__(self):
        assert len(self.operands) > 0, f"{self.__class__} must have at least one expression"

    def roll(self) -> results.MultiplicationRollResult:
        result_items = [results.RollResultItem(result=expression.roll()) for expression in self.operands]

        return results.MultiplicationRollResult(
            result_items=result_items,
        )


__all__ = [
    "MultiplicationExpression",
]
