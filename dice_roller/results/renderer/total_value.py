import dice_roller.results.models as result_models
import dice_roller.results.renderer.base as base_result_renderer


class TotalValueResultRenderer(base_result_renderer.BaseListResultRenderer[int]):
    def _render_value(self, roll: result_models.ValueResult) -> int:
        return roll.value

    def _render_sum(self, roll: result_models.SumResult) -> int:
        result = 0
        for item in roll.result_items:
            if not item.dropped:
                result += self._render_single(item.result)
        return result

    def _render_multiplication(self, roll: result_models.MultiplicationResult) -> int:
        result = 1
        for item in roll.result_items:
            if not item.dropped:
                result *= self._render_single(item.result)
        return result


__all__ = [
    "TotalValueResultRenderer",
]
