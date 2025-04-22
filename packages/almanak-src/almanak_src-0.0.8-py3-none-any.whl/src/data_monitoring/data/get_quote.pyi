from _typeshed import Incomplete
from src.almanak_library.enums import Chain as Chain, Network as Network
from src.utils.logger import get_logger as get_logger
from src.utils.utils import get_web3_by_network_and_chain as get_web3_by_network_and_chain, load_dotenv as load_dotenv

logger: Incomplete

def get_quote_single_input(token0_address: str, token1_address: str, fee: int, amount: int, chain: Chain, network: Network, sqrtPriceLimitX96: int = 0) -> int:
    '''
    A function to call the quoteExactInputSingle function from the uniswap v3
    uni_quoter smart contract.
    #https://docs.uniswap.org/contracts/v3/reference/periphery/lens/Quoter

    Gives the price one would obtain (without slippage). Includes price impact
    and fees in calculation

    Parameters
    ------------
    token0_address: str
        the address of the input token
    token1_address: str
        the address of the output token
    fee: int
        the pool fee where the swap will occur
    amount: int
        the desired input amount


    Returns
    ------------
    quote: int
        the price in units of the second token.
        I.e, "quote / 10**token1_decimals" is in nominal units

    '''
