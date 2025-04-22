import pandas as pd
from _typeshed import Incomplete
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger

ENABLE_DEBUG: Incomplete
logger: Incomplete

def get_daily_burns(daily_df, burns_df) -> pd.DataFrame: ...
