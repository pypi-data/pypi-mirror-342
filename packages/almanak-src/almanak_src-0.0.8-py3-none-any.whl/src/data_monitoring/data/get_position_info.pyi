from _typeshed import Incomplete
from src.almanak_library.enums import Chain as Chain, Network as Network
from src.data_monitoring.data.utils import TICK_SPACING_MAP as TICK_SPACING_MAP, calculate_token0_amount as calculate_token0_amount, calculate_token1_amount as calculate_token1_amount, tick_to_price as tick_to_price, tick_to_unadjusted_sqrtp as tick_to_unadjusted_sqrtp
from src.utils.logger import get_logger as get_logger
from src.utils.utils import get_web3_by_network_and_chain as get_web3_by_network_and_chain, load_dotenv as load_dotenv

logger: Incomplete
Q96: Incomplete
Q128: Incomplete

def process_position_raw_data(raw_position):
    """Receive raw position list data from smart contract and process it into a dictionary.

    Args:
        raw_position (array): Array of 12 elements representing a position.

    Returns:
        dict: Dictionary with keys for easy access of the position info values.
    """
def process_position_readable_data(position: dict, pool_current_tick: int, pool_tick_spacing: int, token0_decimals: int, token1_decimals: int):
    """Add prices for ranges and amounts to the position info.
    Instead of only ticks and liquidity (as provided by the pool smart contract).

    Args:
        position (dict): position info dictionary.
        pool_current_tick (int): current tick of the pool.
        pool_tick_spacing (int): tick spacing of the pool.
        token0_decimals (int): token0 decimals.
        token1_decimals (int): token1 decimals.

    Returns:
        dict: same dictionary with prices and amounts added.
    """
def unsigned_modulo(python_int: int, num_bits: int) -> int:
    """
    Fixed point arithmetic on blockchain is not implemented in python.
    We need to modulo a python integer into an unsigned int of num_bits.

    NOTE: implemented via bitwise.

    Args:
        python_int (int): any python int.
        num_bits (int): The number of bits that the unsigned int needs to be.

    Returns:
        int: An integer in the range [0,..., 2^num_bits -1]
            e.g,. an unsigned int.
    """
def get_unclaimed_fees(pool_contract, position_info) -> tuple[int, int]:
    """
    For a uniswapv3 liquidity position, find the amount of uncollected fees that exists in
    a certain position. Returns the unclaimed fees in units of base token (e.g., WEI for WETH).

    Args:
        pool_contract: web3 contract instantiated for the pool.
        position_info: the raw array the pool returns for a position.

    Returns:
        Tuple[int, int]:
            uncollected_fees0: the amount of uncollected fees the agent has in the position in token0 units,
                                e.g., WEI units for WETH
            uncollected_fees1: the amount of uncollected fees the agent has in the position in token1 units
                                e.g., WEI units for WETH


    NOTE:
    #https://ethereum.stackexchange.com/questions/101955/trying-to-make-sense-of-uniswap-v3-fees-feegrowthinside0lastx128-feegrowthglob
    #https://github.com/someben/pyuv3/blob/main/pyuv3/flowint.py

    #Check out the relevant formulas below which are from Uniswap Whitepaper Section 6.3 and 6.4
    # 𝑓𝑟 =𝑓𝑔−𝑓𝑏(𝑖𝑙)−𝑓𝑎(𝑖𝑢)
    # 𝑓𝑢 =𝑙·(𝑓𝑟(𝑡1)−𝑓𝑟(𝑡0))
    """
def get_lp_token_amounts(pos_liquidity: int, pos_lower_tick: int, pos_upper_tick: int, pool_current_tick: int, pool_tick_spacing: int) -> tuple[int, int]:
    """
    Find the number of tokens inside a single liquidity position.
    NOTE: Copied from the Uniswap SDK, slightly modified (removed the contract calls).

    Returns:
        Tuple[int, int]:
            amount0 - the number of tokens0 in the position
            amount1 - the number of tokens1 in the position
            NOTE: amounts are in base units, e.g., WEI for WETH

    NOTE:
    The logic for getting the token amounts inside a specific tick bin is
    See 3.3.3 of LIQUIDITY MATH IN UNISWAP V3 by Atis Elsts
    """
def get_position_info(wallet_address: str, pool_address: str, chain: Chain, network: Network) -> dict:
    """Get positions info for a wallet address on a specific pool.
    Note: Only 1 position is supported for now. Will raise an error if more (or less) than 1 position is found.

    Args:
        wallet_address (str): Wallet address to monitor.
        pool_address (str): Pool address to monitor. (i.e. ignoring positions on other pools)

    Returns:
        dict: Dictionary with position info.
    """
