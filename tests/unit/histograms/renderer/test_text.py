import dice_roller.histograms as histograms


def test_render_histogram():
    expected = """1: 1 (10.00%)\n2: 2 (20.00%)\n3: 3 (30.00%)\n4: 4 (40.00%)\nTotal: 10"""
    histogram = histograms.Histogram(outcomes={1: 1, 2: 2, 3: 3, 4: 4})
    renderer = histograms.TextHistogramRenderer()

    result = renderer.render(histogram)
    assert result == expected
