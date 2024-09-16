import dataclasses
import typing

import dice_roller.results.models as result_models
import dice_roller.results.renderer.base as base_result_renderer

STRIKETHROUGH = "\u0336"


@dataclasses.dataclass(frozen=True)
class DetailedResult:
    value: int
    details: str


@dataclasses.dataclass(frozen=True)
class DetailedResultRenderer(base_result_renderer.BaseListResultRenderer[DetailedResult]):

    def _format_details(self, details: str, dropped: bool) -> str:
        if dropped:
            return STRIKETHROUGH.join(details) + STRIKETHROUGH

        return details

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
            rendered_item = self._render_single(item.result)

            if not item.dropped:
                value = value_operator(value, rendered_item.value)

            details.append(self._format_details(rendered_item.details, item.dropped))

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
