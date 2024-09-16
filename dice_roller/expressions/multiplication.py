import dataclasses
import functools

import dice_roller.expressions.base as dice_base
import dice_roller.histograms as histograms
import dice_roller.results as results


@dataclasses.dataclass(frozen=True)
class MultiplicationExpression(dice_base.BaseOperationExpression):
    def __post_init__(self):
        assert len(self.operands) > 0, f"{self.__class__} must have at least one expression"

    def roll(self) -> results.MultiplicationResult:
        result_items = [results.ResultItem(result=expression.roll()) for expression in self.operands]

        return results.MultiplicationResult(
            result_items=result_items,
        )

    def get_histogram(self) -> histograms.Histogram:
        return functools.reduce(
            histograms.Histogram.__mul__,
            (expression.get_histogram() for expression in self.operands),
        )


__all__ = [
    "MultiplicationExpression",
]
