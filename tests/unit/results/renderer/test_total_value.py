import dice_roller.results as results


def test_render_multiresult():
    renderer = results.TotalValueResultRenderer()
    roll = results.MultiResult(
        results=[
            results.ValueResult(value=1),
            results.ValueResult(value=2),
            results.ValueResult(value=3),
        ],
    )
    assert renderer.render(roll) == [1, 2, 3]


def test_render_value_roll():
    renderer = results.TotalValueResultRenderer()
    result = results.ValueResult(value=42)
    expected = 42
    assert renderer.render_single(result) == expected
    assert renderer.render(result) == [expected]


def test_render_sum_roll():
    renderer = results.TotalValueResultRenderer()
    roll = results.SumResult(
        result_items=[
            results.ResultItem(result=results.ValueResult(value=1)),
            results.ResultItem(result=results.ValueResult(value=2)),
            results.ResultItem(result=results.ValueResult(value=3)),
        ],
    )
    expected = 6
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]


def test_render_sum_roll_with_dropped():
    renderer = results.TotalValueResultRenderer()
    roll = results.SumResult(
        result_items=[
            results.ResultItem(result=results.ValueResult(value=1)),
            results.ResultItem(result=results.ValueResult(value=2), dropped=True),
            results.ResultItem(result=results.ValueResult(value=3)),
        ],
    )
    expected = 4
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]


def test_render_multiplication_roll():
    renderer = results.TotalValueResultRenderer()
    roll = results.MultiplicationResult(
        result_items=[
            results.ResultItem(result=results.ValueResult(value=2)),
            results.ResultItem(result=results.ValueResult(value=3)),
            results.ResultItem(result=results.ValueResult(value=4)),
        ],
    )
    expected = 24
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]


def test_render_multiplication_roll_with_dropped():
    renderer = results.TotalValueResultRenderer()
    roll = results.MultiplicationResult(
        result_items=[
            results.ResultItem(result=results.ValueResult(value=2)),
            results.ResultItem(result=results.ValueResult(value=3), dropped=True),
            results.ResultItem(result=results.ValueResult(value=4)),
        ],
    )
    expected = 8
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]


def test_render_nested():
    renderer = results.TotalValueResultRenderer()
    roll = results.MultiplicationResult(
        result_items=[
            results.ResultItem(result=results.ValueResult(value=2)),
            results.ResultItem(
                result=results.SumResult(
                    result_items=[
                        results.ResultItem(result=results.ValueResult(value=3)),
                        results.ResultItem(result=results.ValueResult(value=4)),
                    ],
                )
            ),
        ],
    )
    expected = 14
    assert renderer.render_single(roll) == expected
    assert renderer.render(roll) == [expected]
