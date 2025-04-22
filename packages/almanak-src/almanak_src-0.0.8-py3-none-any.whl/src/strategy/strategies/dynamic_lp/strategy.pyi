from _typeshed import Incomplete
from src.almanak_library.constants import ETH_ADDRESS as ETH_ADDRESS
from src.almanak_library.metrics.metrics_agg import METRICS_DB_CONNECTION_STRING as METRICS_DB_CONNECTION_STRING, MetricsAggHandler as MetricsAggHandler
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.strategy.strategies.dynamic_lp.metrics import log_strategy_balance_metrics as log_strategy_balance_metrics
from src.strategy.strategies.dynamic_lp.models import ModelConfig as ModelConfig, PersistentState as PersistentState, State as State, StrategyConfig as StrategyConfig, SubState as SubState
from src.strategy.strategies.dynamic_lp.states import check_for_rebalance as check_for_rebalance, close_position as close_position, initialization as initialization, open_position as open_position, swap_assets as swap_assets, teardown as teardown
from src.strategy.strategy_base import StrategyUniV3 as StrategyUniV3
from src.strategy.utils.pool_token import Token as Token, pooltoken_service as pooltoken_service
from src.strategy.utils.price_volatility import get_current_price as get_current_price
from src.strategy.utils.utils import DataFormat as DataFormat, DataSource as DataSource, convert_time_window as convert_time_window, to_readable as to_readable
from src.utils.config import Config as Config
from src.utils.utils import get_protocol_sdk as get_protocol_sdk, get_web3_by_network_and_chain as get_web3_by_network_and_chain

DEBUG_SHOW_PERSISTENT_STATE: Incomplete

class StrategyDynamicLP(StrategyUniV3):
    STRATEGY_NAME: str
    name: Incomplete
    config: Incomplete
    State: Incomplete
    SubState: Incomplete
    id: Incomplete
    chain: Incomplete
    network: Incomplete
    protocol: Incomplete
    wallet_address: Incomplete
    pause_strategy: Incomplete
    run_duration: Incomplete
    max_sadflow_retries: Incomplete
    max_not_included_retries: Incomplete
    granularity: Incomplete
    time_window: Incomplete
    volatility_factor: Incomplete
    pool_address: Incomplete
    rebalance_frequency: Incomplete
    rebalance_price_bounds: Incomplete
    initialization: Incomplete
    price_model: Incomplete
    volatility_model: Incomplete
    slippage_swap: float
    slippage_open: float
    slippage_close: float
    slippage_spot_rate: float
    lp_bounds_ratio: float
    executioner_status: Incomplete
    metrics_agg_handler: Incomplete
    web3: Incomplete
    uniswap_v3: Incomplete
    pooltoken: Incomplete
    pool: Incomplete
    token0: Incomplete
    token1: Incomplete
    fee: Incomplete
    token_native_WETH: Incomplete
    token_native_ETH: Incomplete
    persistent_state: Incomplete
    def __init__(self, **kwargs) -> None:
        """
        Initializes the Strategy object with the given parameters (via **kargs).

        Args:
            **kwargs: Additional keyword arguments for strategy parameters which must be validated!
            Read the strategy description above for the required parameters.
        """
    @classmethod
    def get_persistent_state_model(cls): ...
    @classmethod
    def get_config_model(cls): ...
    def restart_cycle(self) -> None:
        """A Strategy should only be restarted when the full cycle is completed."""
    def run(self) -> dict:
        """
        Executes the strategy by progressing through its state machine based on the current state.

        This method orchestrates the transitions between different states of the strategy,
        performing actions as defined in each state, and moves to the next state based on the
        actions' results and strategy's configuration.

        Returns:
            dict: A dictionary containing the current state, next state, and actions taken or
                recommended, depending on the execution mode.

        Raises:
            ValueError: If an unknown state is encountered, indicating a potential issue in state management.

        Notes:
            - This method is central to the strategy's operational logic, calling other methods
            associated with specific states like initialization, rebalancing, or closing positions.
            - It integrates debugging features to display balances and positions if enabled.
        """
    def complete(self) -> None: ...
    def get_initialize_amount(self, tokenX: Token, tokenX_available: int, value_USD: float) -> int:
        """
        Calculates the amount of a specific token needed to reach a specified USD value in the portfolio,
        considering the current market price of the token.

        Args:
            tokenX_symbol (str): Symbol of the token for which the amount is being calculated.
            tokenX_available (int): The amount of the token currently available/allocated for this strategy, in smallest unit (e.g., Wei for Ether).
            tokenX_decimals (int): The number of decimal places the token uses.
            value_USD (float): The target value in USD that needs to be reached with the token.

        Returns:
            int: The additional amount of the token required to reach the target USD value, in native format.
                 NOTE: Could be negative if the token amount available/provided exceeds the target value.

        IMPORTANT:
            - If the DataSource is Binance, we assume USD means USDT. (no correcting factor yet USDT/USD)
        """
    def get_available_capital(self, include_last_swap_amounts: bool, verbose: bool = True) -> tuple:
        '''
        Calculates the "new total capital": close + last unallocated + swap readjustment
        '''
    def get_token(self, token_symbol: str = None, token_address: str = None) -> Token:
        """
        Returns a Token object, either self.token0 or self.token1, using either the token_symbol or token_address.
        At least one of token_symbol or token_address must be provided, if both are provided, the token_address is used.

        Args:
            token_symbol (str): The symbol of the token.
            token_address (str, optional): The address of the token. Defaults to None.

        Returns:
            Token: A Token object corresponding to the specified symbol or address.

        Raises:
            ValueError: If neither or both of token_symbol and token_address are provided.
            ValueError: If no matching token is found.
        """
    def get_funding_token(self) -> Token:
        """
        Returns the token that is being used to fund the LP position.

        Returns:
            Token: The token that is being used to fund the LP position.
        """
    def log_strategy_balance_metrics(self, action_id: str): ...
