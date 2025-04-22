from _typeshed import Incomplete
from src.almanak_library.enums import Chain as Chain, Network as Network
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger
from src.utils.utils import get_web3_by_network_and_chain as get_web3_by_network_and_chain, retry_get_block as retry_get_block

ENABLE_DEBUG: Incomplete
logger: Incomplete

def get_start_prices(pool_address, chain: Chain, network: Network, binance_pairs=[]) -> dict:
    '''Get the current finalized block, the price pool and the current prices from Binance for the pairs in the list.

    Args:
        pool_address (_type_): Pool of interest (only supports 1 pool for now).
        binance_pairs (list, optional): List of Binance pairs to get the current price for.
                                        Important: Needs to be Binance format!
                                        e.g. ["ETHBTC", "ETHUSDT", "BTCUSDT"]

    Returns:
        dict: block_start, pool_spot and binance_pairs.
        e.g.
        {\'block_start\': 19230908, \'pool_spot\': 18.630911981398906,
        \'binance_pairs\': {\'ETHBTC\': \'0.05350000\', \'ETHUSDT\': \'2795.09000000\', \'BTCUSDT\': \'52249.12000000\'}}
    '''
