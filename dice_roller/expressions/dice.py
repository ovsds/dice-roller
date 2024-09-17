import dataclasses
import random

import dice_roller.histograms as histograms
import dice_roller.results as results


@dataclasses.dataclass(frozen=True)
class DiceExpression:
    sides: int

    def __post_init__(self):
        assert self.sides > 0, "Number of sides must be positive"

    def roll(self) -> results.ValueResult:
        return results.ValueResult(value=random.randint(1, self.sides))

    def get_histogram(self) -> histograms.Histogram:
        assert self.sides < histograms.HISTOGRAM_LIMIT, "Too many outcomes to calculate histogram"
        return histograms.Histogram({i: 1 for i in range(1, self.sides + 1)})


__all__ = [
    "DiceExpression",
]
