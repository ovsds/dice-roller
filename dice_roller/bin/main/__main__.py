import click

import dice_roller


@click.group()
def main():
    pass


@main.command(name="roll")
@click.argument("raw_expression", type=str)
def roll(raw_expression: str):
    click.echo(f"Rolling {raw_expression}...", err=True)

    expression = dice_roller.parse(raw_expression)
    result = expression.roll()

    detailed_renderer = dice_roller.DetailedRollResultRenderer()
    detailed_result = detailed_renderer.render(result)

    click.echo(f"Details: {detailed_result.details}", err=True)
    click.echo(detailed_result.value)


@main.command(name="histogram")
@click.argument("raw_expression", type=str)
def histogram(raw_expression: str):
    click.echo(f"Building histogram for {raw_expression}...", err=True)

    expression = dice_roller.parse(raw_expression)
    histogram = expression.get_histogram()

    renderer = dice_roller.TextHistogramRenderer()
    text_histogram = renderer.render(histogram)

    click.echo(text_histogram)


if __name__ == "__main__":
    main()
