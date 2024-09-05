import dataclasses
import typing

import dice_roller.results.models as result_models
import dice_roller.results.renderer.base as base_result_renderer

STRIKETHROUGH = "\u0336"


def make_strikethrough(text: str) -> str:
    # add STRIKETHROUGH after each character
    return STRIKETHROUGH.join(text) + STRIKETHROUGH


@dataclasses.dataclass(frozen=True)
class DetailedRollResult:
    value: int
    details: str


class DetailedRollResultRenderer(base_result_renderer.BaseRollResultRenderer[DetailedRollResult]):
    def render_value_roll(self, roll: result_models.ValueRollResult) -> DetailedRollResult:
        return DetailedRollResult(value=roll.value, details=str(roll.value))

    def _render_collection_roll(
        self,
        roll: result_models.BaseCollectionRollResult,
        details_separator: str,
        value_operator: typing.Callable[[int, int], int],
        start_value: int,
    ) -> DetailedRollResult:
        value = start_value
        details: list[str] = []

        for item in roll.result_items:
            rendered_item = self.render(item.result)

            if item.dropped:
                details.append(make_strikethrough(rendered_item.details))
            else:
                value = value_operator(value, rendered_item.value)
                details.append(rendered_item.details)

        result_details = details_separator.join(details)
        result_details = f"({result_details})"

        return DetailedRollResult(value=value, details=result_details)

    def render_sum_roll(self, roll: result_models.SumRollResult) -> DetailedRollResult:
        return self._render_collection_roll(
            roll=roll,
            details_separator="+",
            value_operator=int.__add__,
            start_value=0,
        )

    def render_multiplication_roll(self, roll: result_models.MultiplicationRollResult) -> DetailedRollResult:
        return self._render_collection_roll(
            roll=roll,
            details_separator="*",
            value_operator=int.__mul__,
            start_value=1,
        )


__all__ = [
    "DetailedRollResult",
    "DetailedRollResultRenderer",
]
