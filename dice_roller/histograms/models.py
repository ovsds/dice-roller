import dataclasses
import typing

import typing_extensions


@dataclasses.dataclass(frozen=True)
class Histogram:
    outcomes: dict[int, int]  # value -> count

    def _combine(
        self,
        other: typing_extensions.Self,
        operator: typing.Callable[[int, int], int],
    ) -> typing_extensions.Self:
        outcomes: dict[int, int] = {}

        for value, count in self.outcomes.items():
            for other_value, other_count in other.outcomes.items():
                combined_value = operator(value, other_value)
                combined_count = count * other_count

                outcomes[combined_value] = outcomes.get(combined_value, 0) + combined_count

        return self.__class__(outcomes=outcomes)

    def __add__(self, other: typing.Any) -> typing_extensions.Self:
        if isinstance(other, self.__class__):
            return self._combine(other, operator=int.__add__)

        raise NotImplementedError

    def __mul__(self, other: typing.Any) -> typing_extensions.Self:
        if isinstance(other, self.__class__):
            return self._combine(other, operator=int.__mul__)

        raise NotImplementedError


__all__ = [
    "Histogram",
]
