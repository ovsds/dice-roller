import dice_roller.results as results


def test_render_multiresult():
    renderer = results.DetailedResultRenderer()
    roll = results.MultiResult(
        results=[
            results.ValueResult(value=1),
            results.ValueResult(value=2),
            results.ValueResult(value=3),
        ],
    )
    assert renderer.render(roll) == [
        results.DetailedResult(value=1, details="1"),
        results.DetailedResult(value=2, details="2"),
        results.DetailedResult(value=3, details="3"),
    ]


def test_render_value_roll():
    renderer = results.DetailedResultRenderer()
    roll = results.ValueResult(value=42)
    expected = results.DetailedResult(value=42, details="42")
    assert renderer.render(roll) == [expected]


def test_render_sum_roll():
    renderer = results.DetailedResultRenderer()
    roll = results.SumResult(
        result_items=[
            results.ResultItem(result=results.ValueResult(value=1)),
            results.ResultItem(result=results.ValueResult(value=2)),
            results.ResultItem(result=results.ValueResult(value=3)),
        ],
    )

    expected = results.DetailedResult(value=6, details="(1+2+3)")
    assert renderer.render(roll) == [expected]


def test_render_sum_roll_with_dropped():
    renderer = results.DetailedResultRenderer()
    roll = results.SumResult(
        result_items=[
            results.ResultItem(result=results.ValueResult(value=1)),
            results.ResultItem(result=results.ValueResult(value=2), dropped=True),
            results.ResultItem(result=results.ValueResult(value=3)),
        ],
    )

    expected = results.DetailedResult(value=4, details="(1+2̶+3)")
    assert renderer.render(roll) == [expected]


def test_render_multiplication_roll():
    renderer = results.DetailedResultRenderer()
    roll = results.MultiplicationResult(
        result_items=[
            results.ResultItem(result=results.ValueResult(value=2)),
            results.ResultItem(result=results.ValueResult(value=3)),
            results.ResultItem(result=results.ValueResult(value=4)),
        ],
    )

    expected = results.DetailedResult(value=24, details="(2*3*4)")
    assert renderer.render(roll) == [expected]


def test_render_multiplication_roll_with_dropped():
    renderer = results.DetailedResultRenderer()
    roll = results.MultiplicationResult(
        result_items=[
            results.ResultItem(result=results.ValueResult(value=2)),
            results.ResultItem(result=results.ValueResult(value=3), dropped=True),
            results.ResultItem(result=results.ValueResult(value=4)),
        ],
    )

    expected = results.DetailedResult(value=8, details="(2*3̶*4)")
    assert renderer.render(roll) == [expected]


def test_render_nested():
    renderer = results.DetailedResultRenderer()

    roll = results.SumResult(
        result_items=[
            results.ResultItem(
                result=results.MultiplicationResult(
                    result_items=[
                        results.ResultItem(result=results.ValueResult(value=2)),
                        results.ResultItem(result=results.ValueResult(value=3)),
                    ],
                ),
            ),
            results.ResultItem(result=results.ValueResult(value=4)),
        ],
    )

    expected = results.DetailedResult(value=10, details="((2*3)+4)")
    assert renderer.render(roll) == [expected]
