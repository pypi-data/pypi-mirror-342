from src.almanak_library.constants import ETH_ADDRESS as ETH_ADDRESS, get_address_by_chain_and_network as get_address_by_chain_and_network
from src.almanak_library.enums import ActionType as ActionType, ExecutionStatus as ExecutionStatus, SwapSide as SwapSide, TransactionType as TransactionType
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.models.params import ClosePositionParams as ClosePositionParams, SwapParams as SwapParams, UnwrapParams as UnwrapParams
from src.strategy.strategies.dynamic_lp.metrics import log_close_metrics as log_close_metrics, log_swap_metrics as log_swap_metrics, log_teardown_metrics as log_teardown_metrics, log_unwrap_metrics as log_unwrap_metrics
from src.strategy.strategies.dynamic_lp.strategy import StrategyDynamicLP as StrategyDynamicLP
from src.strategy.utils.utils import create_approve_1token_action as create_approve_1token_action, to_readable as to_readable

def teardown(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Concludes the strategy by closing any active positions and preparing the system for a reset or shutdown.
    Leaves the system in a state where it can be cleanly initialized again.

    1. Close Position
    2. Swap back to Funding Asset.
    3. Unwrap needed? (if Funding Asset is ETH)

    Returns:
        Optional[Action]: An action object configured to close the current liquidity position if one exists,
        or None if no positions are open.
    """
def prepare_close(strat: StrategyDynamicLP) -> ActionBundle: ...
def validate_close(strat: StrategyDynamicLP) -> bool:
    """
    Validates the close position actions and retrieves the amounts from closing the position (liquidity + fees),
    using transaction receipts. It loads the transaction statuses from the executioner and processes them.

    Returns:
        bool: True if the close position actions were successful and the amounts were retrieved correctly.

    Notes:
        The only possible ExecutionStatus at this point is ExecutionStatus.SUCCESS
        otherwise should be in sadflow redoing the actions.
    """
def sadflow_close(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Handles the sadflow for the close substate.
    Calls the appropriate function based on the status of the actions.
    """
def sadflow_close_retry(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Handles the basic retry sadflow.
    """
def sadflow_close_partial_retry(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Handles the complex partial retry sadflow.

    Close position with Multicall has no partial sadflow, it's all or nothing.
    """
def prepare_swap(strat: StrategyDynamicLP, token_index: int) -> ActionBundle:
    """
    Prepares the swap actions. Either the swap0 or swap1 based on the token_index.
    Swaps the assets back to the initial funding token.

    Returns:
        ActionBundle or None: An ActionBundle containing the approve and swap actions if a swap is needed.
    """
def validate_swap(strat: StrategyDynamicLP, token_index: int) -> bool:
    """
    Validates the swap actions and retrieves the executed amounts using the execution details.

    Returns:
        bool: True if the swap actions were successful and the amounts were retrieved correctly.
              and we can move to the next substate.
    """
def sadflow_swap(strat: StrategyDynamicLP, token_index: int) -> ActionBundle:
    """
    Handles the sadflow for the teardown swap0/1 substates.
    Calls the appropriate function based on the status of the actions.
    """
def sadflow_swap_retry(strat: StrategyDynamicLP, token_index: int) -> ActionBundle:
    """
    Handles the basic retry sadflow.
    """
def sadflow_swap_partial_retry(strat: StrategyDynamicLP, token_index: int) -> ActionBundle:
    """
    Handles the complex partial retry sadflow.

    The Prepare Action sends: actions=[action_approve, action_swap]
    - Failure #1: The Approves failed -> We retry the same state as is.
    - Failure #2: Swap failed -> We check the revert reason.
                              -> For now we simply retry the same state as is (updating values),
                                 because we don't care too much double approving.
                  Known revert reasons:
                    - STF: Retry the same state for now.
                    - Slippage: Retry the same state for now.
    """
def prepare_unwrap(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Prepares the unwrap actions for converting WETH back to ETH.

    Returns:
        ActionBundle or None: An ActionBundle containing the unwrap action if an unwrap is needed.
    """
def validate_unwrap(strat: StrategyDynamicLP) -> bool:
    """
    Validates the unwrap actions and retrieves the executed amounts using the execution details.

    Returns:
        bool: True if the unwrap actions were successful and the amounts were retrieved correctly.
    """
def sadflow_unwrap(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Handles the sadflow for the teardown unwrap substate.
    Calls the appropriate function based on the status of the actions.
    """
def sadflow_unwrap_retry(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Handles the basic retry sadflow.
    """
def sadflow_unwrap_partial_retry(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Handles the complex partial retry sadflow.

    Unwrap has no partial sadflow, it's all or nothing.
    """
