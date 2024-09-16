import dataclasses
import typing

import dice_roller.results.models as result_models
import dice_roller.results.renderer.base as base_result_renderer

STRIKETHROUGH = "\u0336"


def make_strikethrough(text: str) -> str:
    # add STRIKETHROUGH after each character
    return STRIKETHROUGH.join(text) + STRIKETHROUGH


@dataclasses.dataclass(frozen=True)
class DetailedResult:
    value: int
    details: str


class DetailedResultRenderer(base_result_renderer.BaseResultRenderer[DetailedResult, list[DetailedResult]]):
    def render(self, roll: result_models.BaseResult) -> list[DetailedResult]:
        if isinstance(roll, result_models.MultiResult):
            return [self.render_single(item) for item in roll.results]

        if isinstance(roll, result_models.BaseSingleResult):
            return [self.render_single(roll)]

        return [self._unsupported(roll)]  # pragma: no cover

    def _render_value(self, roll: result_models.ValueResult) -> DetailedResult:
        return DetailedResult(value=roll.value, details=str(roll.value))

    def _render_collection_roll(
        self,
        roll: result_models.BaseCollectionResult,
        details_separator: str,
        value_operator: typing.Callable[[int, int], int],
        start_value: int,
    ) -> DetailedResult:
        value = start_value
        details: list[str] = []

        for item in roll.result_items:
            rendered_item = self.render_single(item.result)

            if item.dropped:
                details.append(make_strikethrough(rendered_item.details))
            else:
                value = value_operator(value, rendered_item.value)
                details.append(rendered_item.details)

        result_details = details_separator.join(details)
        result_details = f"({result_details})"

        return DetailedResult(value=value, details=result_details)

    def _render_sum(self, roll: result_models.SumResult) -> DetailedResult:
        return self._render_collection_roll(
            roll=roll,
            details_separator="+",
            value_operator=int.__add__,
            start_value=0,
        )

    def _render_multiplication(self, roll: result_models.MultiplicationResult) -> DetailedResult:
        return self._render_collection_roll(
            roll=roll,
            details_separator="*",
            value_operator=int.__mul__,
            start_value=1,
        )


__all__ = [
    "DetailedResult",
    "DetailedResultRenderer",
]
