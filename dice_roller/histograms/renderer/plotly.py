import dataclasses

import plotly.graph_objects as plotly_graph_objects

import dice_roller.histograms.models as histogram_models
import dice_roller.histograms.renderer.base as base


@dataclasses.dataclass
class PlotlyHistogramRenderer(base.BaseHistogramRenderer[bytes]):
    format: str = "png"
    width: int = 1600
    height: int = 1200
    engine: str = "kaleido"

    # skipping coverage for this method as it is not possible to test it in a CI environment
    def render(self, histogram: histogram_models.Histogram) -> bytes:  # pragma: no cover
        x = list(histogram.outcomes.keys())

        total_y = sum(histogram.outcomes.values())
        y = [count / total_y * 100 for count in histogram.outcomes.values()]
        text = [f"{count} ({percentage:.2f}%)" for count, percentage in zip(histogram.outcomes.values(), y)]

        figure = plotly_graph_objects.Figure(
            data=[
                plotly_graph_objects.Bar(
                    x=x,
                    y=y,
                    text=text,
                    textposition="outside",
                )
            ]
        )
        return figure.to_image(
            format=self.format,
            width=self.width,
            height=self.height,
            engine=self.engine,
        )


__all__ = [
    "PlotlyHistogramRenderer",
]
