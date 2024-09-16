import abc
import dataclasses
import typing


class BaseRollResult: ...


class BaseSingleRollResult(BaseRollResult): ...


@dataclasses.dataclass(frozen=True)
class ValueRollResult(BaseSingleRollResult):
    value: int


@dataclasses.dataclass(frozen=True)
class RollResultItem:
    result: BaseSingleRollResult
    dropped: bool = False

    def __post_init__(self):
        if self.dropped:
            assert isinstance(self.result, ValueRollResult), "Dropped result must be a value"


@dataclasses.dataclass(frozen=True)
class BaseCollectionRollResult(abc.ABC, BaseSingleRollResult):
    result_items: typing.Sequence[RollResultItem]

    def __post_init__(self):
        assert any(not roll.dropped for roll in self.result_items), "At least one non-dropped results is required"


class SumRollResult(BaseCollectionRollResult): ...


class MultiplicationRollResult(BaseCollectionRollResult): ...


@dataclasses.dataclass(frozen=True)
class MultiRollResult(BaseRollResult):
    results: typing.Sequence[BaseSingleRollResult]


__all__ = [
    "BaseCollectionRollResult",
    "BaseRollResult",
    "BaseSingleRollResult",
    "MultiRollResult",
    "MultiplicationRollResult",
    "RollResultItem",
    "SumRollResult",
    "ValueRollResult",
]
