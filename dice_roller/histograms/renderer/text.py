import dice_roller.histograms.models as histogram_models
import dice_roller.histograms.renderer.base as base


class TextHistogramRenderer(base.BaseHistogramRenderer[str]):
    def render(self, histogram: histogram_models.Histogram) -> str:
        total = sum(histogram.outcomes.values())

        lines: list[str] = []
        for outcome, count in histogram.outcomes.items():
            percentage = count / total * 100
            lines.append(f"{outcome}: {count} ({percentage:.2f}%)")

        lines.append(f"Total: {total}")

        return "\n".join(lines)


__all__ = [
    "TextHistogramRenderer",
]
