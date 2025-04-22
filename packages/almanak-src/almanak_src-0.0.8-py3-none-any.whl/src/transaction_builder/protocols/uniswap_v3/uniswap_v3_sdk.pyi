from _typeshed import Incomplete
from src.almanak_library.constants import get_address_by_chain_and_network as get_address_by_chain_and_network
from src.almanak_library.enums import Chain as Chain, Network as Network
from src.almanak_library.models.sdk import ISDK as ISDK
from src.utils.config import Config as Config
from src.utils.utils import get_blocknative_tip as get_blocknative_tip, get_web3_by_network_and_chain as get_web3_by_network_and_chain, retry_get_block as retry_get_block
from web3.contract import Contract as Contract

DEBUG: Incomplete

class UniswapV3SDK(ISDK):
    """
    A Uniswap SDK containing the functions that will be called on the uniswap protocol.
    NOTE: Common error codes from uniswap contract: https://docs.uniswap.org/contracts/v3/reference/error-codes
    """
    UNISWAP_TICK_SPACING: Incomplete
    MAX_UINT_128: Incomplete
    MAX_UINT_256: Incomplete
    UNISWAP_MIN_TICK: int
    UNISWAP_MAX_TICK: Incomplete
    Q96: Incomplete
    Q128: Incomplete
    DEADLINE_100_DAYS: int
    web3: Incomplete
    UNISWAP_V3_FACTORY_ADDRESS: Incomplete
    UNISWAP_V3_ROUTER_ADDRESS: Incomplete
    UNISWAP_V3_POSITION_MANAGER_ADDRESS: Incomplete
    UNISWAP_V3_QUOTERV2_ADDRESS: Incomplete
    WETH_ADDRESS: Incomplete
    chain: Incomplete
    network: Incomplete
    deadline: Incomplete
    GAS_BUFFER: float
    APPROVAL_BUFFER: float
    FEE_BUFFER: float
    ERC20_ABI: Incomplete
    POOL_ABI: Incomplete
    def __init__(self, network: Network, chain: Chain) -> None: ...
    @property
    def factory_contract(self) -> Contract: ...
    @property
    def router_contract(self) -> Contract: ...
    @property
    def position_manager_contract(self) -> Contract: ...
    @property
    def quoter_contract(self) -> Contract: ...
    def transfer_eth(self, from_address: str, to_address: str, amount: int, nonce_counter: int = 0, set_gas_override: int | None = None, block_identifier: int | None = None) -> str:
        """
        Transfer ETH from one address to another.

        Parameters
        ------------
        from_address: str
            the address to transfer from
        to_address: str
            the address to transfer to
        amount: int
            the amount of ETH to transfer

        Returns
        ------------
        tx_hash: str
            the transaction hash
        """
    def wrap(self, from_address: str, amount: int, set_gas_override: int | None = None, block_identifier: int | None = None) -> str:
        """
        Wrap ETH to WETH

        Parameters
        ------------
        amount: int
            the amount of ETH to wrap

        Returns
        ------------
        tx_hash: str
            the transaction hash

        """
    def unwrap(self, token_address: str, from_address: str, amount: int, set_gas_override: int | None = None, block_identifier: int | None = None) -> str:
        """
        Unwrap WETH to ETH or other token

        Parameters
        ------------
        amount: int
            the amount of wrap token to unwrap

        Returns
        ------------
        tx_hash: str
            the transaction hash

        """
    def approve(self, token_address: str, spender_address: str, from_address: str, amount: int | None = None, set_gas_override: int | None = None, block_identifier: int | None = None) -> str:
        """
        Approve a spender to spend a certain amount of tokens on behalf of the user.

        Parameters
        ------------
        token_contract: Contract
            the address of the token to approve
        spender_contract: Contract
            the address of the spender
        from_address: str
            the address of the user
        amount: int
            the amount of tokens to approve. If not provided, defaults to the maximum uint256 value

        Returns
        ------------
        tx_hash: str
            the transaction hash

        """
    def swap_in(self, tokenIn: str, tokenOut: str, fee: int, recipient: str, amountIn: int, amountOutMinimum: int, sqrtPriceLimitX96: int, from_address: str, transfer_eth_in: bool, slippage: float | None = None, set_gas_override: int | None = None, block_identifier: int | None = None):
        """
        Builds an unsigned transaction for a single-path swap on Uniswap V3 using the exactInputSingle function.

        Args:
            tokenIn (str): The address of the input token.
            tokenOut (str): The address of the output token.
            fee (int): The fee tier of the pool, e.g., 3000 for 0.3%.
            recipient (str): The address to receive the output tokens.
            amountIn (int): The amount of input tokens to swap, in the smallest indivisible unit.
            amountOutMinimum (int): The minimum amount of output tokens to receive, in the smallest indivisible unit.
            this field is not used right now.
            sqrtPriceLimitX96 (int): The maximum or minimum sqrt price limit, depending on the swap direction.
            from_address (str): The address to send the transaction from.
            transfer_eth_in (bool): Whether to transfer ETH as the input token (if tokenIn is WETH).

        Returns:
            dict: The unsigned transaction dictionary.

        Notes:
            - The transaction fees are calculated using the `get_transaction_fees` method.
            - The gas limit is estimated and increased by the `GAS_BUFFER` factor.
            - If `transfer_eth_in` is True and `tokenIn` is WETH, the transaction value is set to `amountIn`.
            - The transaction type is set to 2 (EIP-1559).
            - The nonce is set to the current transaction count for the `from_address`.
        """
    def quoteExactInputSingle(self, token0_address: str, token1_address: str, fee: int, amount: int, sqrtPriceLimitX96: int = 0, block_identifier: int | None = None) -> int:
        '''
        A function to call the quoteExactInputSingle function from the uniswap v3
        uni_quoter V2 smart contract.
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
    def quoteExactInputSingleV1(self, token0_address: str, token1_address: str, fee: int, amount: int, sqrtPriceLimitX96: int = 0, block_identifier: int | None = None) -> int:
        ''' "
        Quoter function on the uniswap V1 Quoter contract
        '''
    def quoteExactOutputSingle(self, token0_address: str, token1_address: str, fee: int, amount: int, sqrtPriceLimitX96: int = 0, block_identifier: int | None = None) -> int:
        """
        A function to call the quoteExactOutputSingle function from the uniswap v3
        uni_quoter smart contract.
        #https://docs.uniswap.org/contracts/v3/reference/periphery/lens/Quoter

        Given the amount you want to get out, produces a quote for the amount in for a swap over a single pool

        Parameters
        ------------
        token0_address: str
            the address of the input token
        token1_address: str
            the address of the output token
        fee: int
            the pool fee where the swap will occur
        amount: int
            the desired output amount


        Returns
        ------------
        quote: int
            The amount required as the input for the swap in order to receive amountOut

        """
    def quoteExactOutputSingleV1(self, token0_address: str, token1_address: str, fee: int, amount: int, sqrtPriceLimitX96: int = 0, block_identifier: int | None = None) -> int: ...
    def open_lp_position(self, token0_address: str, token1_address: str, fee: int, lower_bound_price: float, upper_bound_price: float, token0_desired: int, token1_desired: int, agent_address: str, amount0_min: int = 0, amount1_min: int = 0, slippage: float | None = None, set_gas_override: int | None = None, block_identifier: int | None = None) -> str:
        """
        Open an lp position on uniswap v3.

        Ordering of the pool matters.
        E.g., if token0_address=WETH, but the pool address token0 = DAI,
        the amounts and tick ranges are inverted within this function.

        ### NOTE: DOES NOT WORK WITH ETH. Do not send ETH in.
        # https://docs.uniswap.org/contracts/v3/guides/providing-liquidity/mint-a-position

        Args:
            token0_address (str):
                token 0 address
            token1_address (str):
                token 1 address
            fee (int):
                pool fee (e.g. 3000 = 0.3%)
            lower_bound_price (float):
                the lower bound of the price to add liquidity in.
                Note price is in nominal units, e.g., 1WETH = 1500.001 USDT
            upper_bound_price (float):
                the upper bound of the price to add liquidity in
                Note price is in nominal units, e.g., 1WETH = 1500.001 USDT
            token0_desired (int):
                the amount of token0 to add into the position in units of token0
                Eg., 1ETH is 10**18 WEI, so token0 = 10**18 for 1 ETH.
            token1_desired (int):
                the amount of token1 to add into the position
            agent_address (str):
                address of the agent
            amount0_min (int, optional): _description_. Defaults to 0.
            amount1_min (int, optional): _description_. Defaults to 0.
            slippage: A number between 0 and 1 which determines amountmin = (1-slippage)*desired

        Returns:
            str: transaction hash of the transaction
        """
    def close_lp_position(self, agent_address: str, position_id: int, amount0_min: int | None = None, amount1_min: int | None = None, slippage: float | None = None, pool_address: str | None = None, set_gas_override: int | None = None, block_identifier: int | None = None) -> list[str]:
        """
        This function removes the liquidity from position_id,
        collects the fees and tokens from the removed liquidity position_id,
        and burns position_id.

        Args:
            agent_address (str):
                The address of the agent position
            position_id (int):
                the integer value of the liquidity position
            amount0_min (int, optional):
                amount0 of token0 to get out for slippage protection. Defaults to 0.
            amount1_min (int, optional):
                amount1 of token1 to get our for slippage protection. Defaults to 0.
            slippage: (float, optional):
                A number between 0 and 1. Defaults to None.
                (1-slippage)*desired will override min amounts.
            pool_address (str, optional):
                The address of the pool, needed only for Slippage calculation. Defaults to None.
                If slippage isn't provided, this is not needed.

        Returns:
            List[str]: [remove_tx_hash, collect_tx_hash, burn_tx_hash]
                transaction hashes of the different transactions

        # NOTE: positions is an ERC721 token:
        https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v1.12.0/contracts/token/ERC721/ERC721Token.sol
        """
    def close_lp_position_multicall(self, agent_address: str, position_id: int, amount0_min: int | None = None, amount1_min: int | None = None, slippage: float | None = None, pool_address: str | None = None, set_gas_override: int | None = None, block_identifier: int | None = None) -> str: ...
    def remove_lp_liquidity(self, agent_address: str, position_id: int, amount0_min: int | None = None, amount1_min: int | None = None, slippage: float | None = None, pool_address: str | None = None, set_gas_override: int | None = None, block_identifier: int | None = None) -> str:
        """
        Removes ALL liquidity from the position_id of agent_address.
        Partial liquidity removal is NOT implemented.

        NOTE: Does not move tokens to agents wallet. To do that, call
                collect(). This function only decreases liquidity position
                on uniswapv3 internal bookkeeping.

        Args:
            agent_address (str):
                The address of the agent of the liquidity position
            position_id (int):
                The id of the liquidity position to be removed
            amount0_min (int, optional):
                Defaults to 0.
            amount1_min (int, optional):
                Defaults to 0.
            liquidity (int):
                The amount of liquidity to be removed.

        Returns:
            str:
                The transaction hash of the position
        """
    def collect_lp(self, agent_address: str, position_id: int, set_gas_override: int | None = None, block_identifier: int | None = None) -> str:
        """
        After having accumulated fees, or having decreased a liquidity position,
        the tokens are still in uniswapv3 position and need to be moved to agents wallet.
        This function moves/collects the maximum amount of
        both fees and liquidity to the agents
        wallet from uniswap contract.

        Args:
            agent_address (str): agents address
            position_id (int): id of the agents position which the own.

        Returns:
            str: transaction hash of the transaction.
        """
    def burn_lp_position(self, agent_address: str, position_id: int, set_gas_override: int | None = None, block_identifier: int | None = None) -> str:
        """
        Burn the liquidity position of agent_address at position_id
        NOTE: can't burn until all liquidity is removed and fees collected

        Args:
            agent_address (str):
                address of agent of the position
            position_id (int):
                id of the position of the agent_address

        Returns:
            str:
                transaction hash of the burn transaction
        """
    def get_unclaimed_fees(self, pool_address: str, position_id: int, block_identifier: int | None = None) -> tuple[int, int]:
        """
        For a uniswapv3 liquidity position, find the amount of uncollected fees that exists in
        a certain position. Returns the unclaimed fees in units of base token (e.g., WEI for WETH).
        Args:
            pool_address (str): address of the uniswap v3 pool
            position_id (int): position of the agents liquidity.
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
    def get_lp_token_amounts(self, pool_address: str, position_id: int, block_identifier: int | None = None) -> tuple[int, int]:
        """
        Find the number of tokens inside a single liquidity position for an agent.
        Args:
            pool_address (str):
                The address of the specific pool of interest
            position_id (int):
                the id of the lp position of the agent
        Returns:
            Tuple[int, int]:
                amount0 - the number of tokens0 in the position
                amount1 - the number of tokens1 in the position
                NOTE: amounts are in base units, e.g., WEI for WETH
        NOTE:
        The logic for getting the token amounts inside a specific tick bin is
        See 3.3.3 of LIQUIDITY MATH IN UNISWAP V3 by Atis Elsts
        """
    def calculate_token0_amount(self, liquidity, sp, sa, sb):
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
    def calculate_token1_amount(self, liquidity, sp, sa, sb):
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
    def calculate_liquidity0(self, amount0, sa, sb): ...
    def calculate_liquidity1(self, amount1, sa, sb): ...
    def calculate_liquidity(self, amount0, amount1, sp, sa, sb):
        """
        https://github.com/uniyj/uni-v3-peri/blob/main/atiselsts-uniswap-v3-liquidity-math/uni-v3-liquidity-math.ipynb
        """
    def get_position_info(self, position_id: int, block_identifier: int | None = None) -> tuple: ...
    def get_positions(self, agent_address: str, block_identifier: int | None = None) -> list[int]:
        """get indices of agent's LP positions (i.e. position IDs)"""
    def get_pool_spot_rate(self, pool_address: str, inverted: bool = False, block_identifier: Incomplete | None = None) -> float: ...
    def get_pool_current_tick(self, pool_address: str) -> int: ...
    def get_pool(self, token0_address: str, token1_address: str, fee: int): ...
    def is_checksum_address(self, address: str) -> bool: ...
    def to_checksum_address(self, address: str) -> str: ...
    def get_pool_liquidity(self, pool_address: str): ...
    def get_transaction_fees(self, block_identifier: Incomplete | None = None) -> dict[str, int]: ...
    def get_token_contract(self, token_address: str) -> Contract: ...
    def get_pool_contract(self, pool_address: str) -> Contract: ...
    def pool_price_from_current_tick(self, token0_address: str, token1_address: str, pool_fee: int, block_identifier: Incomplete | None = None) -> tuple[float, int]:
        """
            Return the price of the current tick, in the order of the token input addresses.

        Args:
            token0_address (str): _description_
            token1_address (str): _description_
            pool_fee (int): _description_

        Returns:
            float: the price of the pool in the order of the input tokens.
            int: the current tick of the pool.
        """
    def unsigned_modulo(self, python_int: int, num_bits: int) -> int:
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
    def get_min_tick(self, fee: int) -> int: ...
    def get_max_tick(self, fee: int) -> int: ...
    def default_tick_range(self, fee: int) -> tuple[int, int]: ...
    def nearest_tick(self, tick: int, fee: int) -> int:
        """
        Return the nearest tick on the uniswap v3 pool.
        """
    def price_to_tick(self, price: float, token0_decimals: int, token1_decimals: int) -> int:
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
    def price_to_sqrtp(self, price): ...
    def sqrtp_to_price(self, sqrtp): ...
    def tick_to_unadjusted_sqrtp(self, tick: int) -> float:
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
    def tick_to_price(self, tick: int, token0_decimals: int, token1_decimals: int) -> float:
        """
        Determine the price given a tick value.

        Args:
            tick (int): the tick of the pool from which to calculate price
            token0_decimals (int):
            token1_decimals (int):
        """
    def tick_to_sqrt_price(self, tick: int) -> float: ...
    def tick_to_sqrt_price_x_96(self, tick): ...
    def sqrt_price_x_96_to_tick(self, sqrt_price_x_96): ...
    def price_x96_to_price(self, sqrt_price_x_96, decimals_diff: int = 12): ...
    def trunc_int(self, num: int) -> int: ...
    def get_next_ticks(self, pool_address: str, fee: int, buffer: int, side_lower: bool, tick: int = None):
        '''
        This function calculates from either the current tick or a given tick, the next valid ticks based on the buffer.

        Args:
            pool_address (str): The address of the pool.
            fee (int): The fee of the pool.
            buffer (int): The number of bins or tick spacing to "skip".
            side_lower (bool): The side of the buffer relative to the tick.
            tick (int): None will default to the current tick from on-chain fetching.

        :return: The tick of the next bin to place the 1-sided position.
        '''
    def lp_fees_percent_of_current_tokens(self, pool_address: str, position_id: int, block_identifier: int | None = None) -> tuple[float, float]: ...
    def calculate_impermanent_loss(self, price: float, strike_price: float, lower_limit: float, upper_limit: float, dex: str = 'uniswap_v3') -> float:
        '''
        Calculate the impermanent loss for a single Uniswap V3 position.

        NOTE: Impermanent loss is defined to be a negative number here.

        Args:
            price (float): price (current)
            strike_price (float): "strike price" (i.e. price the position was opened at)
            lower_limit (float): lower bound of Uniswap V3 position range
            upper_limit (float): upper bound of Uniswap V3 position range
            dex (str): DEX in which to calculate IL (e.g. \'uniswap_v2\', default == \'uniswap_v3\')

        Returns:
            float: impermanent loss as a fraction. To get a percentage, multiply by 100
        '''
    def calculate_open_position_amount(self, token0_amount: int, token1_amount: int, lower_price: float, upper_price: float, pool_address: str, slippage_spot_rate: float, adjust_amounts: bool = True, adjust_threshold: float = 0.001, block_identifier: int | None = None) -> tuple[tuple[int, int], tuple[float, float], float]:
        """
        Calculate the amount of tokens to be deposited into a Uniswap V3 position.
        Input a range of spot price that could be realized in the future, and output a range of liquidity amounts that
        could be deposited into the position.
        """
    def calculate_open_position_amount_with_spot_rate(self, token0_amount: int, token1_amount: int, lower_price: float, upper_price: float, pool_address: str, spot_rate: float, adjust_amounts: bool = True, adjust_threshold: float = 0.001) -> tuple[tuple[int, int], tuple[float, float]]: ...
