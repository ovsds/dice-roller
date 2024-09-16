import dataclasses

import dice_roller.histograms as histograms
import dice_roller.results as results


@dataclasses.dataclass(frozen=True)
class ConstantExpression:
    value: int

    def roll(self) -> results.ValueResult:
        return results.ValueResult(self.value)

    def get_histogram(self) -> histograms.Histogram:
        return histograms.Histogram({self.value: 1})


__all__ = [
    "ConstantExpression",
]
