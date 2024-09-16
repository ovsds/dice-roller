import dataclasses

import dice_roller.expressions.base as base_expression
import dice_roller.results as results


@dataclasses.dataclass(frozen=True)
class RepeatedExpression:
    expression: base_expression.SingleExpressionProtocol
    count: int = 1

    def __post_init__(self):
        assert self.count > 0, "Number of expression repetition must be positive"

    def roll(self) -> results.MultiResult:
        return results.MultiResult(results=[self.expression.roll() for _ in range(self.count)])

    def get_histogram(self) -> base_expression.histograms.Histogram:
        return self.expression.get_histogram()


__all__ = [
    "RepeatedExpression",
]
