import abc
import dataclasses
import typing


class BaseRollResult: ...


@dataclasses.dataclass(frozen=True)
class ValueRollResult(BaseRollResult):
    value: int


@dataclasses.dataclass(frozen=True)
class RollResultItem:
    result: BaseRollResult
    dropped: bool = False

    def __post_init__(self):
        if self.dropped:
            assert isinstance(self.result, ValueRollResult), "Dropped result must be a value"


@dataclasses.dataclass(frozen=True)
class BaseCollectionRollResult(abc.ABC, BaseRollResult):
    result_items: typing.Sequence[RollResultItem]

    def __post_init__(self):
        assert any(not roll.dropped for roll in self.result_items), "At least one non-dropped results is required"


class SumRollResult(BaseCollectionRollResult): ...


class MultiplicationRollResult(BaseCollectionRollResult): ...


__all__ = [
    "BaseCollectionRollResult",
    "BaseRollResult",
    "MultiplicationRollResult",
    "RollResultItem",
    "SumRollResult",
    "ValueRollResult",
]
