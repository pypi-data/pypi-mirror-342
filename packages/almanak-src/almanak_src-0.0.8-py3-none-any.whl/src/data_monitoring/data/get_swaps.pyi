import pandas as pd
from _typeshed import Incomplete
from src.data_monitoring.data.utils import get_graphql_client as get_graphql_client
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger

ENABLE_DEBUG: Incomplete
logger: Incomplete

def get_swaps(pool_address, start_timestamp: Incomplete | None = None, end_timestamp: Incomplete | None = None) -> pd.DataFrame: ...
