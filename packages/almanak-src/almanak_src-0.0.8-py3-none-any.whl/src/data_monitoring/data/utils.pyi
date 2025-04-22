from _typeshed import Incomplete
from src.data_monitoring.data.constants import GRAPHQL_ENDPOINT as GRAPHQL_ENDPOINT
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger

ENABLE_DEBUG: Incomplete
logger: Incomplete
UNISWAP_TICK_SPACING: Incomplete
MAX_UINT_128: Incomplete
MAX_UINT_256: Incomplete
UNISWAP_MIN_TICK: int
UNISWAP_MAX_TICK: Incomplete
Q96: Incomplete
Q128: Incomplete
TICK_SPACING_MAP: Incomplete

def unix_to_datetime(unix_timestamp): ...
def to_unix_timestamp(date_str, date_format: str = '%d/%m/%Y %H:%M:%S %Z'): ...
def get_graphql_client(): ...
def price_to_tick(price: float, token0_decimals: int, token1_decimals: int) -> int:
    """
    Converts a price in nominal units to a tick value on
    uniswap v3

    Args:
        price (float):
            The price of token0 to token1 in nominal units.
            E.g., 1eth = 1500.01 usdt
        token0_decimals (int): decimals of token0
        token1_decimals (int): decimals of token1

    Returns:
        int:
        the tick value for the inputted price
    """
def tick_to_price(tick: int, token0_decimals: int, token1_decimals: int) -> float:
    """
    Determine the price given a tick value.

    Args:
        tick (int): the tick of the pool from which to calculate price
        token0_decimals (int):
        token1_decimals (int):
    """
def calculate_token0_amount(liquidity, sp, sa, sb):
    """
    Calculate the number of tokens0 inside an individual tick bin

    Args:
        liquidity (_type_): liquidity in position
        sp (_type_): sqrt of current price
        sa (_type_): sqrt of lower tick price
        sb (_type_): sqrt of upper tick price

    Returns:
        number of tokens0 in tick bin
    """
def calculate_token1_amount(liquidity, sp, sa, sb):
    """
    Calculate the number of tokens1 inside an individual tick bin

    Args:
        liquidity (_type_): liquidity in position
        sp (_type_): sqrt of current price
        sa (_type_): sqrt of lower tick price
        sb (_type_): sqrt of upper tick price

    Returns:
        number of tokens1 in tick bin
    """
def tick_to_unadjusted_sqrtp(tick: int) -> float:
    """
        Convert a tick to an unadjusted sqrt price.
        Unadjusted means no token decimals multiplication
        has been performed.

    Args:
        tick (int): A tick bin.

    Returns:
        unadjusted_price:
            The price that has not been adjusted yet.
            See 3.3.2 of LIQUIDITY MATH IN UNISWAP V3 by Atis Elsts

    NOTE: To convert to an actual price, need to multiply by
        token0.decimals - token1.decimals as in tick_to_price() function
    """
