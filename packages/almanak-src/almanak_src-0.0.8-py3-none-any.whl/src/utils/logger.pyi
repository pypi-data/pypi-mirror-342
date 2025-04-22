import logging
from _typeshed import Incomplete
from src.utils.config import Config as Config

ENABLE_REDACTING: Incomplete
IS_GCS_PROXY: Incomplete
IS_SQL_PROXY: Incomplete
IS_AGENT_DEPLOYMENT: Incomplete
MAX_FILTER_LENGTH: int
ENV_ITEMS: Incomplete

def redact_env_values(message: str) -> str: ...
def redacting_log_method(self, severity, message, *args, **kwargs): ...

class RedactingStream:
    original_stream: Incomplete
    env_items: Incomplete
    def __init__(self, original_stream) -> None: ...
    def write(self, text) -> None: ...
    def flush(self) -> None: ...

def redacting_print(*args, **kwargs) -> None: ...

class EnvRedactionFilter(logging.Filter):
    def filter(self, record): ...

class RedactingManager(logging.Manager):
    def getLogger(self, name): ...

old_manager: Incomplete
new_manager: Incomplete

class MaxLevelFilter(logging.Filter):
    max_level: Incomplete
    def __init__(self, max_level) -> None: ...
    def filter(self, record): ...

class DowngradeRetryInternalFilter(logging.Filter):
    def filter(self, record): ...

class SuppressEulithWebsocketErrors(logging.Filter):
    def filter(self, record): ...

class AdjustUrllib3WarningLevel(logging.Filter):
    def filter(self, record): ...

def setup_logging() -> None: ...
def get_logger(logger_name): ...
def setup_non_alert_logger(logger_name):
    """
    Sets up a non-alert logger that downgrades all log messages to INFO level.
    Automatically appends '_non_alert' to the logger name to avoid conflicts.
    """
def get_non_alert_logger(logger_name):
    """
    Retrieves the non-alert logger corresponding to the given logger_name.
    Automatically adjusts the logger name to avoid conflicts.
    """
