import abc
import dataclasses
import typing


class BaseResult: ...


class BaseSingleResult(BaseResult): ...


@dataclasses.dataclass(frozen=True)
class ValueResult(BaseSingleResult):
    value: int


@dataclasses.dataclass(frozen=True)
class ResultItem:
    result: BaseSingleResult
    dropped: bool = False

    def __post_init__(self):
        if self.dropped:
            assert isinstance(self.result, ValueResult), "Dropped result must be a value"


@dataclasses.dataclass(frozen=True)
class BaseCollectionResult(abc.ABC, BaseSingleResult):
    result_items: typing.Sequence[ResultItem]

    def __post_init__(self):
        assert any(not roll.dropped for roll in self.result_items), "At least one non-dropped results is required"


class SumResult(BaseCollectionResult): ...


class MultiplicationResult(BaseCollectionResult): ...


@dataclasses.dataclass(frozen=True)
class MultiResult(BaseResult):
    results: typing.Sequence[BaseSingleResult]


__all__ = [
    "BaseCollectionResult",
    "BaseResult",
    "BaseSingleResult",
    "MultiResult",
    "MultiplicationResult",
    "ResultItem",
    "SumResult",
    "ValueResult",
]
