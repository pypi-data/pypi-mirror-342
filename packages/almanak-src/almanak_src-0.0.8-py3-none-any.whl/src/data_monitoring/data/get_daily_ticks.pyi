import pandas as pd
from _typeshed import Incomplete
from src.data_monitoring.data.get_ticks import get_ticks as get_ticks
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger

ENABLE_DEBUG: Incomplete
logger: Incomplete

def get_daily_ticks(daily_df: pd.DataFrame, lower_tick, upper_tick) -> pd.DataFrame: ...
