import pandas as pd
from _typeshed import Incomplete
from src.data_monitoring.data.get_block_from_timestamp import get_block_from_timestamp as get_block_from_timestamp
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger

ENABLE_DEBUG: Incomplete
logger: Incomplete

def get_daily_block_start(api_key, daily_df, rate_limit: int = 0) -> pd.DataFrame: ...
