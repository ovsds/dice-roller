import dice_roller
import dice_roller.histograms as histograms
import dice_roller.results as results


def test_roll():
    dice = dice_roller.ConstantExpression(value=3)
    assert dice.roll() == results.ValueResult(value=3)


def test_get_histogram():
    dice = dice_roller.ConstantExpression(value=3)
    assert dice.get_histogram() == histograms.Histogram({3: 1})
