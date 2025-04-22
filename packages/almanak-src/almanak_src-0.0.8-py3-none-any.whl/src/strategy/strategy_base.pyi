import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from src.almanak_library.enums import ExecutionStatus as ExecutionStatus
from src.almanak_library.metrics.metrics_agg import MetricAggType as MetricAggType, MetricsAggTable as MetricsAggTable
from src.almanak_library.metrics.metrics_logger import MetricsLogger as MetricsLogger
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.profiler.time_block import ProfileType as ProfileType
from src.almanak_library.profiler.utils import time_block as time_block
from src.executer.execution_manager import ExecutionManager as ExecutionManager
from src.strategy.models import InternalFlowStatus as InternalFlowStatus, Mode as Mode, StateBase as StateBase, SubStateBase as SubStateBase
from src.strategy.utils.price_volatility import get_current_price as get_current_price
from src.strategy.utils.utils import to_readable as to_readable
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger
from src.utils.utils import download_action_bundle_from_storage as download_action_bundle_from_storage

STORAGE_DIR: Incomplete
READ_ONLY_MODE: Incomplete
PERSISTENT_STATE_FILENAME: str
IS_AGENT_DEPLOYMENT: Incomplete
logger: Incomplete
storage_client: Incomplete

class Strategy(ABC, metaclass=abc.ABCMeta):
    N_NOT_INCLUDED_UNLOCK_SOFT_RAISE: int
    class NotIncludedUnlockError(Exception):
        """Exception raised when a NOT_INCLUDED still fails after N_NOT_INCLUDED_UNLOCK_SOFT_RAISE retries."""
        message: Incomplete
        def __init__(self, message: str = 'NOT_INCLUDED max retries reached. Soft raise to unblock main thread.') -> None: ...
    InternalFlowStatus: Incomplete
    State: Incomplete
    SubState: Incomplete
    PersistentStateModel: Incomplete
    ConfigModel: Incomplete
    web3: Incomplete
    mode: Incomplete
    simulation: bool
    granularity: str
    wallet_address: Incomplete
    persistent_state: Incomplete
    metrics_agg_handler: Incomplete
    metrics_action_handler: Incomplete
    execution_manager: Incomplete
    metrics_logger: Incomplete
    max_sadflow_retries: int
    max_not_included_retries: int
    pause_strategy: bool
    def __init__(self) -> None: ...
    @abstractmethod
    def run(self): ...
    @abstractmethod
    def restart_cycle(self): ...
    @property
    def is_locked(self):
        """Check if the strategy cycle has completed and now waiting the next."""
    @property
    def is_paused(self): ...
    @property
    def is_initialized(self):
        """Check if the strategy is initialized."""
    @property
    def is_terminated(self):
        """Check if the strategy is terminated (teardown finished)"""
    @classmethod
    @abstractmethod
    def get_persistent_state_model(cls):
        """Pydandic model defined in child's class."""
    @classmethod
    @abstractmethod
    def get_config_model(cls):
        """Pydandic model defined in child's class."""
    def save_persistent_state(self) -> None: ...
    def save_persistent_state_local(self) -> None: ...
    def save_persistent_state_gcs(self) -> None:
        """
        Saves the strategy's persistent state to GCS ensuring that the strategy can resume operation
        from where it last left off after a restart or shutdown.

        Raises:
            FileNotFoundError: If the configuration file is not found at the specified path.
            ValueError: If there is an error decoding JSON from the configuration file.
            EnvironmentError: If required environment variables are not set.
            PermissionsError: If there are insufficient permissions to access the file.
            TimeoutError: If the request to download the configuration file times out.
            GoogleAPICallError: For network-related errors or issues on the backend from Google Cloud services.
        """
    executioner_status: Incomplete
    def load_persistent_state(self) -> None: ...
    def load_persistent_state_bytes_local(self) -> None: ...
    def load_persistent_state_bytes_gcs(self) -> None:
        """
        Loads the strategy's state from persistent storage in GCS.

        This method is responsible for restoring the state of the strategy from GCS,
        ensuring that the strategy can resume operation from where it last left off after a restart or shutdown.
        """
    def check_for_persistent_state_file(self) -> bool: ...
    def check_for_persistent_state_file_local(self) -> bool: ...
    def check_for_persistent_state_file_gcs(self) -> bool:
        """Mainly a utility function to check if the persistent state file exists."""
    def upload_persistent_state(self, template_path: str, force_upload: bool = False):
        """
        Loads the local json template and saves it as the persistent state.
        That step is meant to be done manually when deploying a strategy!

        Args:
            template_path (str): Path to the JSON template file.
            force_upload (bool): Whether to force upload the persistent state.
        """
    def initialize_persistent_state(self, template_path: str): ...
    def load_executioner_state(self, action_id: str) -> dict:
        """
        Loads the executioner's state from persistent storage in GCS.

        Note: Only supports Pickle format for now as serializing Web3 objects to JSON is not straightforward.
        """
    def validate_executioner_action_bundle(self, action_bundle: ActionBundle):
        """
        This function is called while loading the persistent state, when re-entering the strategy.
        First the Strategy Persistent State is loaded,
        then the Executioner Status is loaded based on the current action_id.
        """
    def handle_state_with_actions(self, prepare_fn, validate_fn, sadflow_fn, next_state, next_substate: Incomplete | None = None): ...
    @abstractmethod
    def log_strategy_balance_metrics(self, action_id: str): ...

class StrategyUniV3(Strategy, metaclass=abc.ABCMeta):
    def __init__(self) -> None: ...
    def get_wallet_active_positions(self):
        """
        Retrieves and identifies all active positions.
        Returns only the one(s) that match the strategy's pool and with liquidity (i.e. active).

        IMPORTANT: This is wallet-level, not strategy-level.

        Returns:
            Dict[int, Tuple]: A dictionary of active positions where keys are position IDs and values are
            the position details. The position details are the default one returned by Uniswap V3 enhanced
            with 2 additional values appended: token0 and token1 amount (from liquidity value to token amount).
        """
    def get_active_position_info(self, position_id: int): ...
    def calculate_desired_amounts(self, amount0_initial: int, amount1_initial: int, ratio: float, spot_price: float, token0_decimals: int, token1_decimals: int) -> tuple[int, int]:
        """
        Calculates the desired amounts based on a specified ratio and the current spot price,
        using Decimal for intermediate calculations and converting the result back to int.

        Args:
            amount0_initial (int): The current amount of token0 in native units (e.g., Wei).
            amount1_initial (int): The current amount of token1 in native units (e.g., Wei).
            ratio (float): The desired ratio of token0 to token1 in the pool.
            spot_price (float): The current market spot price of token1 measured in units of token0.
            token0_decimals (int): The number of decimals for token0.
            token1_decimals (int): The number of decimals for token1.

        Returns:
            Tuple[int, int]: The desired amounts of token0 and token1 in native units (e.g., Wei).
        """
    def calculate_reswap_amounts(self, amount0_initial: int, amount1_initial: int, ratio: float, spot_price: float, token0_decimals: int, token1_decimals: int, amount0_desired: int | None = None, amount1_desired: int | None = None) -> tuple[bool | None, int, int]:
        """
        Calculates the specific amounts of tokens to swap to achieve the desired ratio,
        using Decimal for intermediate calculations and converting the result back to int.

        Args:
            amount0_initial (int): The current amount of token0 in native units (e.g., Wei).
            amount1_initial (int): The current amount of token1 in native units (e.g., Wei).
            ratio (float): The target ratio of token0 to token1 that the portfolio should aim to achieve.
            spot_price (float): The current market price of token1 in terms of token0.
            token0_decimals (int): The number of decimals for token0.
            token1_decimals (int): The number of decimals for token1.
            amount0_desired (Optional[int]): The desired amount of token0 in native units (e.g., Wei).
            amount1_desired (Optional[int]): The desired amount of token1 in native units (e.g., Wei).

        Returns:
            Tuple[Optional[bool], int, int]: A tuple containing:
                - A boolean indicating whether token0 needs to be swapped for token1 (True) or vice versa (False).
                - The amount of the input token to be swapped in native units.
                - The amount of the output token to be received in native units.
        """
    def get_balances(self, native_format: bool = False) -> tuple[float, float, float]: ...
    def show_balances(self) -> None: ...
    def show_positions(self) -> None:
        """Display the current positions of the wallet. Debug Function."""
    def show_state(self, show_persistent_state: bool = False):
        """Display the current state and flowstatus of the strategy."""
    def log_snapshot(self, action_id: str | None = None, bundle_id: str | None = None, block_number: int | None = None): ...
