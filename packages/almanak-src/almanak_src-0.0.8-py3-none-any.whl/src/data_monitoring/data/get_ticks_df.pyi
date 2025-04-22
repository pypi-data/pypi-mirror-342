import pandas as pd
from _typeshed import Incomplete
from src.data_monitoring.data.utils import tick_to_price as tick_to_price
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger

ENABLE_DEBUG: Incomplete
logger: Incomplete

def get_ticks_df(daily_df, tick_spacing, decimals0, decimals1, tick_to_bin_swaps: str = 'tick_end') -> pd.DataFrame | None: ...
