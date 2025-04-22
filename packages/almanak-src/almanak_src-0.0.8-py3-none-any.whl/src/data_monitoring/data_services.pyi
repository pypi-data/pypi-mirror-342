import datetime
import pandas as pd
from _typeshed import Incomplete
from src.data_monitoring.data import get_pool_info_onchain as get_pool_info_onchain, get_position_info as get_position_info
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger
from typing import Iterable

ENABLE_DEBUG: Incomplete
logger: Incomplete

def get_data_for_simulation_input(wallet_address: str, pool_addresses: Iterable[str], start_time: datetime.datetime | None, end_time: datetime.datetime | None):
    """Gets the data required for the simulation input. Passed as parameters.

    Args:
        wallet_address (str): Wallet address to monitor.
        pool_addresses (Iterable[str]): Pool addresses to monitor.
        start_time (Optional[datetime.datetime]): Horizon start time for data fetching.
        end_time (Optional[datetime.datetime]): Horizon end time for data fetching.
    """
def get_data_for_rebalancing(wallet_address: str, pool_addresses: Iterable[str]) -> dict[str, tuple[pd.DataFrame, ...]]:
    """
    Gets all the data required by the rebalancing
        1. Current Pool Spot Price.
        2. Current Position Info.
    """
