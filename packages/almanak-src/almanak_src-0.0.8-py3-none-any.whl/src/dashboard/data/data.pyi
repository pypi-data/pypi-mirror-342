from _typeshed import Incomplete
from decimal import Decimal
from src.almanak_library.enums import Chain as Chain, Network as Network, Protocol as Protocol
from src.data_monitoring.data import get_block_from_timestamp as get_block_from_timestamp
from src.utils.utils import Config as Config, get_web3_by_network_and_chain as get_web3_by_network_and_chain, retry_get_block as retry_get_block

TICK_SPACING_MAP: Incomplete
ETHERSCAN_API_CALL_DELAY: float
THEGRAPH_API_KEY: Incomplete
THEGRAPH_BASE_URL: str
THEGRAPH_UNISWAP_V3: Incomplete

def get_thegraph_url(protocol: Protocol, chain: Chain, network: Network) -> str: ...
def tick_to_raw_price_token0(tick: int) -> float: ...
def liquidity_to_token0_token1_adj(liquidity: Decimal, lower_tick: int, upper_tick: int, decimals0: int, decimals1: int) -> tuple[Decimal, Decimal]: ...
def tick_to_price(tick: int, token0_decimals: int, token1_decimals: int) -> Decimal:
    """
    Determine the price given a tick value.

    Args:
        tick (int): the tick of the pool from which to calculate price
        token0_decimals (int):
        token1_decimals (int):
    """
def get_ticks_info(pool_address: str, chain: Chain, network: Network, block: int = None) -> dict: ...

class TickInfo:
    liquidity_net: Incomplete
    liquidity_gross: Incomplete
    tick_idx: Incomplete
    date: Incomplete
    def __init__(self, liquidity_net, liquidity_gross, tick_idx) -> None: ...

class PoolInfo:
    protocol: Incomplete
    chain: Incomplete
    network: Incomplete
    address: Incomplete
    current_tick: int
    tick_spacing: int
    fee_tier: int
    active_tick: int
    liquidity: Decimal
    token0_decimals: int
    token1_decimals: int
    liquidity_token0: Decimal
    liquidity_token1: Decimal
    price_token0: float
    price_token1: float
    pair_name: str
    token0_symbol: str
    token1_symbol: str
    info_data_source: str
    ticks_data_source: str
    thegraph_url: Incomplete
    block: Incomplete
    block_timestamp: Incomplete
    def __init__(self, chain: Chain, network: Network, address: str, tick: int, fee_tier: int, liquidity: Decimal, token0_decimals: int, token1_decimals: int, price_token1: float, price_token0: float, symbol0: str, symbol1: str, info_data_source: str = '', ticks_data_source: str = '', block: int = None) -> None: ...
    @staticmethod
    def get_pool_info_thegraph(pool_address: str, chain: Chain, network: Network, block: int = None): ...
    @staticmethod
    def get_pool_info_onchain(pool_address: str, chain: Chain, network: Network): ...
    @staticmethod
    def get(pool_address: str, chain: Chain, network: Network, block: int = None) -> PoolInfo:
        """
        Get pool statistics from subgraph for uniswap v3 or onchain
        :param pool_address: pool address in 0x format
        :return: PoolInfo
        """
    def process_ticks(self): ...

def process_position_raw_data(raw_position):
    """Receive raw position list data from smart contract and process it into a dictionary.

    Args:
        raw_position (array): Array of 12 elements representing a position.

    Returns:
        dict: Dictionary with keys for easy access of the position info values.
    """
def get_position_info(wallet_address: str, pool_address: str, chain: Chain, network: Network, block_number: int = None) -> dict: ...
def get_position_info_over_time(node_endpoint: str, etherscan_key: str, wallet_address: str, pool_address: str, start_time, end_time, chain: Chain, network: Network) -> dict: ...
