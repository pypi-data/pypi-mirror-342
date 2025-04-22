from _typeshed import Incomplete
from src.almanak_library.constants import MessageStatus as MessageStatus
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger
from src.utils.utils import retry_on_exception as retry_on_exception

logger: Incomplete

class InternalMessaging:
    def __init__(self) -> None: ...
    @staticmethod
    def send_to_slack(channel: str, message: str) -> MessageStatus: ...
    @staticmethod
    async def async_send_to_telegram(bot, channel_id, message) -> None: ...
    @staticmethod
    def send_telegram_message(chat_id, message): ...
    @staticmethod
    def escape_markdown(text):
        """
        Helper function to escape special characters for MarkdownV2.
        """
