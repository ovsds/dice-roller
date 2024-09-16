import dice_roller.results as results


def test_render_multiresult():
    renderer = results.TotalValueRollResultRenderer()
    roll = results.MultiRollResult(
        results=[
            results.ValueRollResult(value=1),
            results.ValueRollResult(value=2),
            results.ValueRollResult(value=3),
        ],
    )
    assert renderer.render(roll) == [1, 2, 3]


def test_render_value_roll():
    renderer = results.TotalValueRollResultRenderer()
    result = results.ValueRollResult(value=42)
    expected = 42
    assert renderer.render_single(result) == expected
    assert renderer.render(result) == [expected]


def test_render_sum_roll():
    renderer = results.TotalValueRollResultRenderer()
    roll = results.SumRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=1)),
            results.RollResultItem(result=results.ValueRollResult(value=2)),
            results.RollResultItem(result=results.ValueRollResult(value=3)),
        ],
    )
    expected = 6
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]


def test_render_sum_roll_with_dropped():
    renderer = results.TotalValueRollResultRenderer()
    roll = results.SumRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=1)),
            results.RollResultItem(result=results.ValueRollResult(value=2), dropped=True),
            results.RollResultItem(result=results.ValueRollResult(value=3)),
        ],
    )
    expected = 4
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]


def test_render_multiplication_roll():
    renderer = results.TotalValueRollResultRenderer()
    roll = results.MultiplicationRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=2)),
            results.RollResultItem(result=results.ValueRollResult(value=3)),
            results.RollResultItem(result=results.ValueRollResult(value=4)),
        ],
    )
    expected = 24
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]


def test_render_multiplication_roll_with_dropped():
    renderer = results.TotalValueRollResultRenderer()
    roll = results.MultiplicationRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=2)),
            results.RollResultItem(result=results.ValueRollResult(value=3), dropped=True),
            results.RollResultItem(result=results.ValueRollResult(value=4)),
        ],
    )
    expected = 8
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]


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
    expected = 14
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]
