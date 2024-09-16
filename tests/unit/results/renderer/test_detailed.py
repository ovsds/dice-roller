import dice_roller.results as results


def test_render_multiresult():
    renderer = results.DetailedRollResultRenderer()
    roll = results.MultiRollResult(
        results=[
            results.ValueRollResult(value=1),
            results.ValueRollResult(value=2),
            results.ValueRollResult(value=3),
        ],
    )
    assert renderer.render(roll) == [
        results.DetailedRollResult(value=1, details="1"),
        results.DetailedRollResult(value=2, details="2"),
        results.DetailedRollResult(value=3, details="3"),
    ]


def test_render_value_roll():
    renderer = results.DetailedRollResultRenderer()
    roll = results.ValueRollResult(value=42)
    expected = results.DetailedRollResult(value=42, details="42")
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]


def test_render_sum_roll():
    renderer = results.DetailedRollResultRenderer()
    roll = results.SumRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=1)),
            results.RollResultItem(result=results.ValueRollResult(value=2)),
            results.RollResultItem(result=results.ValueRollResult(value=3)),
        ],
    )

    expected = results.DetailedRollResult(value=6, details="(1+2+3)")
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]


def test_render_sum_roll_with_dropped():
    renderer = results.DetailedRollResultRenderer()
    roll = results.SumRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=1)),
            results.RollResultItem(result=results.ValueRollResult(value=2), dropped=True),
            results.RollResultItem(result=results.ValueRollResult(value=3)),
        ],
    )

    expected = results.DetailedRollResult(value=4, details="(1+2̶+3)")
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]


def test_render_multiplication_roll():
    renderer = results.DetailedRollResultRenderer()
    roll = results.MultiplicationRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=2)),
            results.RollResultItem(result=results.ValueRollResult(value=3)),
            results.RollResultItem(result=results.ValueRollResult(value=4)),
        ],
    )

    expected = results.DetailedRollResult(value=24, details="(2*3*4)")
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]


def test_render_multiplication_roll_with_dropped():
    renderer = results.DetailedRollResultRenderer()
    roll = results.MultiplicationRollResult(
        result_items=[
            results.RollResultItem(result=results.ValueRollResult(value=2)),
            results.RollResultItem(result=results.ValueRollResult(value=3), dropped=True),
            results.RollResultItem(result=results.ValueRollResult(value=4)),
        ],
    )

    expected = results.DetailedRollResult(value=8, details="(2*3̶*4)")
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]


def test_render_nested():
    renderer = results.DetailedRollResultRenderer()

    roll = results.SumRollResult(
        result_items=[
            results.RollResultItem(
                result=results.MultiplicationRollResult(
                    result_items=[
                        results.RollResultItem(result=results.ValueRollResult(value=2)),
                        results.RollResultItem(result=results.ValueRollResult(value=3)),
                    ],
                ),
            ),
            results.RollResultItem(result=results.ValueRollResult(value=4)),
        ],
    )

    expected = results.DetailedRollResult(value=10, details="((2*3)+4)")
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]
