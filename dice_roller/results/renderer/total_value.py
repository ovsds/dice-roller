import dice_roller.results.models as result_models
import dice_roller.results.renderer.base as base_result_renderer


class TotalValueResultRenderer(base_result_renderer.BaseResultRenderer[int, list[int]]):
    def render(self, roll: result_models.BaseResult) -> list[int]:
        if isinstance(roll, result_models.MultiResult):
            return [self.render_single(item) for item in roll.results]

        if isinstance(roll, result_models.BaseSingleResult):
            return [self.render_single(roll)]

        return [self._unsupported(roll)]  # pragma: no cover

    def _render_value(self, roll: result_models.ValueResult) -> int:
        return roll.value

    def _render_sum(self, roll: result_models.SumResult) -> int:
        result = 0
        for item in roll.result_items:
            if not item.dropped:
                result += self.render_single(item.result)
        return result

    def _render_multiplication(self, roll: result_models.MultiplicationResult) -> int:
        result = 1
        for item in roll.result_items:
            if not item.dropped:
                result *= self.render_single(item.result)
        return result


__all__ = [
    "TotalValueResultRenderer",
]
