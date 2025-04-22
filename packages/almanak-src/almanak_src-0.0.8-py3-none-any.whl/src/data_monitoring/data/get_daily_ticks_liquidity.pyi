import pandas as pd
from _typeshed import Incomplete
from src.data_monitoring.data.utils import calculate_token0_amount as calculate_token0_amount, calculate_token1_amount as calculate_token1_amount, tick_to_unadjusted_sqrtp as tick_to_unadjusted_sqrtp
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger

ENABLE_DEBUG: Incomplete
logger: Incomplete

def get_daily_ticks_liquidity(day_ticks_df, tick_spacing) -> pd.DataFrame: ...
