from src.almanak_library.constants import ETH_ADDRESS as ETH_ADDRESS
from src.almanak_library.enums import ActionType as ActionType, ExecutionStatus as ExecutionStatus, SwapSide as SwapSide, TransactionType as TransactionType
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.models.params import SwapParams as SwapParams
from src.strategy.strategies.dynamic_lp.states.open_position import calculate_position as calculate_position
from src.strategy.strategies.dynamic_lp.strategy import StrategyDynamicLP as StrategyDynamicLP
from src.strategy.utils.utils import create_approve_1token_action as create_approve_1token_action

def swap_assets(strat: StrategyDynamicLP) -> ActionBundle | None:
    """
    Executes the necessary asset swaps to maintain the desired token ratio to open a new position based
    on what was received from closing the previous position.

    Will only swap in the direction of the token that needs to be increased to reach the desired ratio.

    Args:
        strat (StrategyDynamicLP): The Strategy instance.

    Returns:
        ActionBundle or None: An ActionBundle containing the approve and swap actions if a swap is needed.

    Notes:
        - Swaps are done in the pool in which we are LPing. A better routing will be implemented.
    """
def prepare_swap_assets(strat: StrategyDynamicLP) -> ActionBundle | None:
    """
    Prepares the swap actions.

    Returns:
        ActionBundle or None: An ActionBundle containing the approve and swap actions if a swap is needed.
    """
def validate_swap_assets(strat: StrategyDynamicLP) -> bool:
    """
    Validates the swap actions and retrieves the executed amounts using the execution details.

    Returns:
        bool: True if the swap actions were successful and the amounts were retrieved correctly.
              and we can move to the next state.
    """
def sadflow_swap_assets(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Handles the sadflow for the swap assets state.
    Calls the appropriate function based on the status of the actions.
    """
def sadflow_retry(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Handles the basic retry sadflow.
    """
def sadflow_partial_retry(strat: StrategyDynamicLP) -> ActionBundle:
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
