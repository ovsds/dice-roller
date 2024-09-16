import dataclasses
import logging
import sys
import typing

import aiogram
import pydantic_settings
import typing_extensions

import dice_roller
import dice_roller.results as results

logger = logging.getLogger(__name__)


class TelegramAppSettings(pydantic_settings.BaseSettings):
    token: str = NotImplemented

    bot_name: str = "Dice Roller"
    bot_short_description: str = "A simple dice roller bot"
    bot_description: str = "A simple dice roller bot"

    image_width: int = 1280
    image_height: int = 960

    class Config:
        env_prefix = "TELEGRAM_APP_"


class MessageHandlerProtocol(typing.Protocol):
    async def process(self, message: aiogram.types.Message): ...


class TelegramDetailedResultRenderer(results.DetailedResultRenderer):
    def _format_details(self, details: str, dropped: bool) -> str:
        if dropped:
            return f"<s>{details}</s>̶"
        return details


@dataclasses.dataclass(frozen=True)
class TelegramMessageResultRenderer:
    detailed_renderer: TelegramDetailedResultRenderer = dataclasses.field(
        default_factory=TelegramDetailedResultRenderer
    )

    def render(self, roll: results.BaseResult) -> str:
        rendered = self.detailed_renderer.render(roll)
        return "\n".join(f"<b>{item.value}</b>={item.details}" for item in rendered)


@dataclasses.dataclass(frozen=True)
class RollService:
    renderer: results.ResultRendererProtocol[str]

    def roll(self, raw_expression: str) -> str:
        expression = dice_roller.parse(raw_expression)
        result = expression.roll()
        return self.renderer.render(result)


@dataclasses.dataclass(frozen=True)
class HistogramService:
    renderer: dice_roller.PlotlyHistogramRenderer

    def build_histogram(self, raw_expression: str) -> bytes:
        expression = dice_roller.parse(raw_expression)
        histogram = expression.get_histogram()
        return self.renderer.render(histogram)


@dataclasses.dataclass(frozen=True)
class MessageHandler(MessageHandlerProtocol):
    roll_service: RollService
    histogram_service: HistogramService

    async def _process_roll(self, raw_expression: str, message: aiogram.types.Message) -> None:
        try:
            result = self.roll_service.roll(raw_expression)
        except Exception:
            logger.exception("Error while processing roll expression: %s", raw_expression)
            await message.reply("Error while processing roll expression")
        else:
            await message.reply(result, parse_mode=aiogram.enums.ParseMode.HTML)

    async def _process_histogram(self, raw_expression: str, message: aiogram.types.Message) -> None:
        try:
            result = self.histogram_service.build_histogram(raw_expression)
        except Exception:
            logger.exception("Error while processing histogram expression: %s", raw_expression)
            await message.reply("Error while processing histogram expression")
        else:

            await message.reply_photo(
                photo=aiogram.types.BufferedInputFile(result, filename="histogram.png"),
                caption=f"Histogram for: {raw_expression}",
            )

    async def process(self, message: aiogram.types.Message):
        if message.text is None:
            return

        if message.text.startswith("/roll"):
            raw_expression = message.text[5:].strip()
            return await self._process_roll(raw_expression, message)

        if message.text.startswith("/r"):
            raw_expression = message.text[2:].strip()
            return await self._process_roll(raw_expression, message)

        if message.text.startswith("/histogram"):
            raw_expression = message.text[10:].strip()
            return await self._process_histogram(raw_expression, message)

        if message.text.startswith("/h"):
            raw_expression = message.text[2:].strip()
            return await self._process_histogram(raw_expression, message)

        if message.text.startswith("/"):
            raw_expression = message.text[1:].strip()
            return await self._process_roll(raw_expression, message)


@dataclasses.dataclass(frozen=True)
class TelegramApp:
    aiogram_bot: aiogram.Bot
    aiogram_dispatcher: aiogram.Dispatcher
    settings: TelegramAppSettings

    @classmethod
    def from_settings(cls, settings: TelegramAppSettings) -> typing_extensions.Self:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)

        aiogram_bot = aiogram.Bot(token=settings.token)
        aiogram_dispatcher = aiogram.Dispatcher()
        result_renderer = TelegramMessageResultRenderer()
        histogram_renderer = dice_roller.PlotlyHistogramRenderer(
            width=settings.image_width,
            height=settings.image_height,
        )

        roll_service = RollService(renderer=result_renderer)
        histogram_service = HistogramService(renderer=histogram_renderer)

        message_handler = MessageHandler(roll_service=roll_service, histogram_service=histogram_service)

        aiogram_dispatcher.message.register(message_handler.process)

        return cls(
            aiogram_bot=aiogram_bot,
            aiogram_dispatcher=aiogram_dispatcher,
            settings=settings,
        )

    async def start(self):
        try:
            await self._setup_bot()
            await self.aiogram_dispatcher.start_polling(self.aiogram_bot)
        finally:
            await self.dispose()

    async def _setup_bot(self):
        logger.info("Setting up bot...")

        name = await self.aiogram_bot.get_my_name()
        if name.name != self.settings.bot_name:
            await self.aiogram_bot.set_my_name(self.settings.bot_name)

        description = await self.aiogram_bot.get_my_description()
        if description.description != self.settings.bot_description:
            await self.aiogram_bot.set_my_description(self.settings.bot_description)

        short_description = await self.aiogram_bot.get_my_short_description()
        if short_description.short_description != self.settings.bot_short_description:
            await self.aiogram_bot.set_my_short_description(self.settings.bot_short_description)

        commands = await self.aiogram_bot.get_my_commands()
        expected_commands = [
            aiogram.types.BotCommand(command="roll", description="Roll a dice"),
            aiogram.types.BotCommand(command="histogram", description="Build a histogram"),
        ]
        if commands != expected_commands:
            await self.aiogram_bot.set_my_commands(expected_commands)

    async def dispose(self):
        logger.info("Disposing bot...")
        try:
            await self.aiogram_bot.session.close()
        except Exception:
            logger.exception("Error while disposing bot session")


__all__ = [
    "TelegramApp",
    "TelegramAppSettings",
]
