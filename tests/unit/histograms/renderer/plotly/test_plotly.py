import os

import pytest

import dice_roller
import tests.settings as tests_settings


@pytest.fixture(name="skip_plotly")
def skip_plotly_fixture(settings: tests_settings.PytestSettings):
    if settings.environment == tests_settings.Environment.ci:
        pytest.skip("Skipping Plotly tests")


@pytest.mark.usefixtures("skip_plotly")
def test_render_histogram():
    expected_filepath = os.path.join(os.path.dirname(__file__), "expected.png")
    histogram = dice_roller.histograms.Histogram(outcomes={1: 1, 2: 2, 3: 3, 4: 4})
    renderer = dice_roller.PlotlyHistogramRenderer(height=300, width=300)

    result = renderer.render(histogram)

    if not os.path.exists(expected_filepath):
        with open(expected_filepath, "wb") as f:
            f.write(result)

    with open(expected_filepath, "rb") as f:
        expected = f.read()

    assert result == expected
