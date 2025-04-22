from _typeshed import Incomplete
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger

ENABLE_DEBUG: Incomplete
logger: Incomplete

def get_block_from_timestamp(api_key, timestamp, closest: str = 'before') -> int | None: ...
