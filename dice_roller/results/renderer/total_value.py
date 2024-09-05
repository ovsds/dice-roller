import dice_roller.results.models as result_models
import dice_roller.results.renderer.base as base_result_renderer


class TotalValueRollResultRenderer(base_result_renderer.BaseRollResultRenderer[int]):
    def render_value_roll(self, roll: result_models.ValueRollResult) -> int:
        return roll.value

    def render_sum_roll(self, roll: result_models.SumRollResult) -> int:
        result = 0
        for item in roll.result_items:
            if not item.dropped:
                result += self.render(item.result)
        return result

    def render_multiplication_roll(self, roll: result_models.MultiplicationRollResult) -> int:
        result = 1
        for item in roll.result_items:
            if not item.dropped:
                result *= self.render(item.result)
        return result


__all__ = [
    "TotalValueRollResultRenderer",
]
