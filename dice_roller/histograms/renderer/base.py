import abc
import typing

import dice_roller.histograms.models as histogram_models

RenderResultT = typing.TypeVar("RenderResultT")


class BaseHistogramRenderer(typing.Generic[RenderResultT]):
    @abc.abstractmethod
    def render(self, histogram: histogram_models.Histogram) -> RenderResultT: ...


__all__ = [
    "BaseHistogramRenderer",
]
