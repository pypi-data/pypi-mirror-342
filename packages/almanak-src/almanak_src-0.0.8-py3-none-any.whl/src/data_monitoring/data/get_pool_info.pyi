from _typeshed import Incomplete
from src.almanak_library.enums import Chain as Chain, Network as Network
from src.data_monitoring.data.utils import TICK_SPACING_MAP as TICK_SPACING_MAP, get_graphql_client as get_graphql_client
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger
from src.utils.utils import get_web3_by_network_and_chain as get_web3_by_network_and_chain

ENABLE_DEBUG: Incomplete
logger: Incomplete

def get_pool_info(pool_address) -> dict: ...
def get_pool_address(token0_address: str, token1_address: str, fee: int, chain: Chain, network: Network) -> dict: ...
def get_pool_info_onchain(pool_address, chain: Chain, network: Network) -> dict: ...
