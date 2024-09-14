import dice_roller.results.models as result_models
import dice_roller.results.renderer.base as base_result_renderer


class TotalValueRollResultRenderer(base_result_renderer.BaseRollResultRenderer[int]):
    def _render_value(self, roll: result_models.ValueRollResult) -> int:
        return roll.value

    def _render_sum(self, roll: result_models.SumRollResult) -> int:
        result = 0
        for item in roll.result_items:
            if not item.dropped:
                result += self.render(item.result)
        return result

    def _render_multiplication(self, roll: result_models.MultiplicationRollResult) -> int:
        result = 1
        for item in roll.result_items:
            if not item.dropped:
                result *= self.render(item.result)
        return result


__all__ = [
    "TotalValueRollResultRenderer",
]
