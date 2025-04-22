from .states.check_positions import check_positions as check_positions
from .states.close_position import close_position as close_position
from .states.initialization import initialization as initialization
from .states.teardown import teardown as teardown
from _typeshed import Incomplete
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.strategy.strategies.troubleshoot_close_positions.models import PersistentState as PersistentState, State as State, StrategyConfig as StrategyConfig, SubState as SubState
from src.strategy.strategy_base import StrategyUniV3 as StrategyUniV3
from src.utils.utils import get_protocol_sdk as get_protocol_sdk, get_web3_by_network_and_chain as get_web3_by_network_and_chain
from time import sleep as sleep

class StrategyTroubleshootClosePositions(StrategyUniV3):
    STRATEGY_NAME: str
    name: Incomplete
    State: Incomplete
    SubState: Incomplete
    config: Incomplete
    id: Incomplete
    chain: Incomplete
    network: Incomplete
    protocol: Incomplete
    wallet_address: Incomplete
    specific_positions: Incomplete
    specific_pools: Incomplete
    uniswap_v3: Incomplete
    persistent_state: Incomplete
    def __init__(self, **kwargs) -> None:
        """
        Initialize the strategy with given configuration parameters.

        Args:
            **kwargs: Strategy-specific configuration parameters.
        """
    @classmethod
    def get_persistent_state_model(cls): ...
    @classmethod
    def get_config_model(cls): ...
    def restart_cycle(self) -> None:
        """A Strategy should only be restarted when the full cycle is completed."""
    def run(self):
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
    def log_strategy_balance_metrics(self, action_id: str):
        """Logs strategy balance metrics per action. It is called in the StrategyBase class."""
