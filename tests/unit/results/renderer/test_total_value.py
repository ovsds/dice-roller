import dice_roller.results as results


def test_render_value_roll():
    renderer = results.TotalValueRollResultRenderer()
    roll = results.ValueRollResult(value=42)
    assert renderer.render(roll) == 42


def test_render_sum_roll():
    renderer = results.TotalValueRollResultRenderer()
    roll = results.SumRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=1)),
            results.RollResultItem(result=results.ValueRollResult(value=2)),
            results.RollResultItem(result=results.ValueRollResult(value=3)),
        ],
    )
    assert renderer.render(roll) == 6


def test_render_sum_roll_with_dropped():
    renderer = results.TotalValueRollResultRenderer()
    roll = results.SumRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=1)),
            results.RollResultItem(result=results.ValueRollResult(value=2), dropped=True),
            results.RollResultItem(result=results.ValueRollResult(value=3)),
        ],
    )
    assert renderer.render(roll) == 4


def test_render_multiplication_roll():
    renderer = results.TotalValueRollResultRenderer()
    roll = results.MultiplicationRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=2)),
            results.RollResultItem(result=results.ValueRollResult(value=3)),
            results.RollResultItem(result=results.ValueRollResult(value=4)),
        ],
    )
    assert renderer.render(roll) == 24


def test_render_multiplication_roll_with_dropped():
    renderer = results.TotalValueRollResultRenderer()
    roll = results.MultiplicationRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=2)),
            results.RollResultItem(result=results.ValueRollResult(value=3), dropped=True),
            results.RollResultItem(result=results.ValueRollResult(value=4)),
        ],
    )
    assert renderer.render(roll) == 8


def test_render_nested():
    renderer = results.TotalValueRollResultRenderer()
    roll = results.MultiplicationRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=2)),
            results.RollResultItem(
                result=results.SumRollResult(
                    result_items=[
                        results.RollResultItem(result=results.ValueRollResult(value=3)),
                        results.RollResultItem(result=results.ValueRollResult(value=4)),
                    ],
                )
            ),
        ],
    )
    assert renderer.render(roll) == 14
