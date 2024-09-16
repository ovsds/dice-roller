import asyncio

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

    detailed_renderer = dice_roller.DetailedResultRenderer()
    detailed_result = detailed_renderer.render(result)

    for item in detailed_result:
        click.echo(f"Details: {item.details}", err=True)
        click.echo(item.value)


@main.command(name="histogram")
@click.argument("raw_expression", type=str)
def histogram(raw_expression: str):
    click.echo(f"Building histogram for {raw_expression}...", err=True)

    expression = dice_roller.parse(raw_expression)
    histogram = expression.get_histogram()

    renderer = dice_roller.TextHistogramRenderer()
    text_histogram = renderer.render(histogram)

    click.echo(text_histogram)


@main.command(name="telegram")
def telegram():
    click.echo("Starting Telegram bot...", err=True)

    import dice_roller.telegram as telegram

    settings = telegram.TelegramAppSettings()
    app = telegram.TelegramApp.from_settings(settings)

    asyncio.run(app.start())


__all__ = [
    "main",
]
