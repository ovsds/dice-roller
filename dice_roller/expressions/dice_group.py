import collections
import dataclasses
import itertools

import dice_roller.expressions.dice as dice_expression
import dice_roller.histograms as histograms
import dice_roller.results as results

GREEDY_HISTOGRAM_LIMIT = 1_000_000


@dataclasses.dataclass(frozen=True)
class DiceGroupExpression:
    dice: dice_expression.DiceExpression
    count: int
    retain_highest: int = 0
    retain_lowest: int = 0

    def __post_init__(self):
        assert self.count > 0, "Number of expression must be positive"

        assert self.retain_highest >= 0, "Number of dice to retain must be non-negative"
        assert self.retain_lowest >= 0, "Number of dice to retain must be non-negative"

        assert self.retain_highest <= self.count, "Number of dice to retain must be less than the total number of dice"
        assert self.retain_lowest <= self.count, "Number of dice to retain must be less than the total number of dice"

        count = 0
        if self.retain_highest > 0:
            count += 1
        if self.retain_lowest > 0:
            count += 1

        assert not (
            self.retain_highest > 0 and self.retain_lowest > 0
        ), "Only one of drop_highest, retain_highest, drop_lowest, retain_lowest can be used"

    def _get_dropped_rolls(self, rolls: list[results.ValueRollResult]) -> dict[int, int]:
        if self.retain_highest + self.retain_lowest == 0:
            return {}

        sorted_rolls_values = sorted(rolls, key=lambda roll: roll.value)
        dropped_rolls: dict[int, int] = collections.defaultdict(int)

        if self.retain_lowest > 0:
            for roll in sorted_rolls_values[self.retain_lowest :]:
                dropped_rolls[roll.value] += 1

        if self.retain_highest > 0:
            for roll in sorted_rolls_values[: -self.retain_highest]:
                dropped_rolls[roll.value] += 1

        return dropped_rolls

    def roll(self) -> results.SumRollResult:
        roll_results = [self.dice.roll() for _ in range(self.count)]

        dropped_rolls = self._get_dropped_rolls(roll_results)

        result_items: list[results.RollResultItem] = []

        for result in roll_results:
            dropped = False

            if dropped_rolls.get(result.value, 0) > 0:
                dropped_rolls[result.value] -= 1
                dropped = True

            result_items.append(results.RollResultItem(result=result, dropped=dropped))

        return results.SumRollResult(result_items=result_items)

    def get_histogram(self) -> histograms.Histogram:
        return self.get_histogram_greedily()

    def get_histogram_greedily(self) -> histograms.Histogram:
        assert self.dice.sides**self.count < GREEDY_HISTOGRAM_LIMIT, "Too many outcomes to calculate histogram greedily"

        outcomes: dict[int, int] = collections.defaultdict(int)

        for values in itertools.product(*(range(1, self.dice.sides + 1) for _ in range(self.count))):
            sorted_values = sorted(values)
            if self.retain_lowest:
                sorted_values = sorted_values[: self.retain_lowest]
            if self.retain_highest:
                sorted_values = sorted_values[-self.retain_highest :]

            outcomes[sum(sorted_values)] += 1

        return histograms.Histogram(outcomes)


__all__ = [
    "DiceGroupExpression",
]
