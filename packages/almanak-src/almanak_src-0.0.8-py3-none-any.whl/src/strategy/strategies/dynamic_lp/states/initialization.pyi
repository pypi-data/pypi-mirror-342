from _typeshed import Incomplete
from src.almanak_library.constants import ETH_ADDRESS as ETH_ADDRESS, get_address_by_chain_and_network as get_address_by_chain_and_network
from src.almanak_library.enums import ActionType as ActionType, ExecutionStatus as ExecutionStatus, SwapSide as SwapSide, TransactionType as TransactionType
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.models.params import OpenPositionParams as OpenPositionParams, SwapParams as SwapParams, UnwrapParams as UnwrapParams, WrapParams as WrapParams
from src.strategy.strategies.dynamic_lp.metrics import log_initialization_metrics as log_initialization_metrics, log_open_metrics as log_open_metrics, log_swap_metrics as log_swap_metrics
from src.strategy.strategies.dynamic_lp.states.open_position import calculate_position as calculate_position
from src.strategy.strategies.dynamic_lp.strategy import StrategyDynamicLP as StrategyDynamicLP
from src.strategy.utils.utils import create_approve_1token_action as create_approve_1token_action, create_approve_2tokens_actions as create_approve_2tokens_actions, to_readable as to_readable
from src.utils.config import Config as Config

DEBUG: Incomplete

def initialization(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Prepares the strategy by swapping relevant assets to have the deployed capital ready.
    For example, if the allocated amount for the strategy in USD is 100k, we will prepare the wallet
    to have $50k worth of token0 and $50k worth of token1. This is done by swapping the initial funding token
    into token0/1.

    The initialization process has 3 SubStates, see it as a (sub)state machine within this state:
    1. Swap0: Prepare the token0 amount.
    2. Swap1: Prepare the token1 amount.
    3. Open Position: Open the liquidity position with the token0/1 amounts.

    Returns:
        ActionBundle: An action bundle representing a swap or open transaction required to initialize
        the strategy, or None if no actions are required (e.g. suffisant token0/1 are already available).

    Notes:
        - This method MUST ONLY BE CALLED AT THE START OF THE STRATEGY LIFECYCLE to prepare the assets.
        - This method is implemented for re-entry during the initialization phase, with specific SubStates.
    """
def prepare_swap(strat: StrategyDynamicLP, token_index: int) -> ActionBundle:
    """
    Prepares the swap actions. Either the swap0 or swap1 based on the token_index.

    Returns:
        ActionBundle or None: An ActionBundle containing the approve and swap actions if a swap is needed.

    Notes:
        - If the token is the initial funding token, no swap is needed.
        - If the token is ETH and the initial funding token is ETH, we wrap the ETH to WETH.
        - Otherwise, we swap the initial funding token to the token (either token0/1) for a specific USD value.
    """
def validate_swap(strat: StrategyDynamicLP, token_index: int) -> bool:
    """
    Validates the swap actions and retrieves the executed amounts using the execution details.

    Could be a wrap only, a swap only, a wrap and a swap, or no actions at all (e.g. funding == token).

    Returns:
        bool: True if the swap actions were successful and the amounts were retrieved correctly.
              and we can move to the next substate.
    """
def sadflow_swap(strat: StrategyDynamicLP, token_index: int) -> ActionBundle:
    """
    Handles the sadflow for the init swap0/1 substates.
    Calls the appropriate function based on the status of the actions.
    """
def sadflow_swap_retry(strat: StrategyDynamicLP, token_index: int) -> ActionBundle:
    """
    Handles the basic retry sadflow.
    """
def sadflow_swap_partial_retry(strat: StrategyDynamicLP, token_index: int) -> ActionBundle:
    """
    Handles the complex partial retry sadflow.

    *IMPORTANT* the swap can be only a wrap here or include one.
    If the asset to swap into was only a wrap, there is no swap, no approve.

    The Prepare Action has 3 paths:
    1. Approve and Swap: actions=[action_approve, action_swap]
    2. Wrap, Approve and Swap: actions=[action_wrap, action_approve, action_swap]
    3. Wrap: actions=[action_wrap]

    We need to identify which path was taken, as for example an approval fail in a approve & swap is different than
    an approval after a wrap went thru.

    Path #1: Approve and Swap
    Handled in sadflow_swap_partial_retry_handle_AS(...)

    Path #2: Wrap, Approve and Swap
    Handled in sadflow_swap_partial_retry_handle_WAS(...)

    Path #3: Wrap
    Should not end up here since it's 1 transaction only.
    """
def sadflow_swap_partial_retry_handle_AS(strat: StrategyDynamicLP, token_index: int) -> ActionBundle:
    """
    Handles partial retry for Path #1: Approve and Swap

    - Failure #1: The Approves failed -> We retry the same state as is.
    - Failure #2: Swap failed -> We check the revert reason.
                              -> For now we simply retry the same state as is (updating values),
                                 because we don't care too much double approving.
                  Known revert reasons:
                    - STF: Retry the same state for now.
                    - Slippage: Retry the same state for now.
    """
def sadflow_swap_partial_retry_handle_WAS(strat: StrategyDynamicLP, token_index: int) -> ActionBundle:
    """
    Handles partial retry for Path #2: Wrap, Approve and Swap

    - Failure #1: The Wrap failed -> We retry the same state as is.
    - Failure #2: The Approves failed but Wrap successful -> We do no re-wrap!! We can't retry the same state as is.
    - Failure #3: Swap failed failed but Wrap successful -> We do no re-wrap!! We can't retry the same state as is.
    """
def prepare_open(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Prepares the open position actions.

    Returns:
        ActionBundle or None: An ActionBundle containing the approve and swap actions if a swap is needed.
    """
def validate_open(strat: StrategyDynamicLP) -> bool:
    """
    Validates the open position actions and retrieves the executed amounts using transaction receipts.
    It loads the transaction statuses from the executioner and processes them.

    Returns:
        bool: True if the open position actions were successful and the amounts were retrieved correctly.

    Raises:
        ValueError: If the number of transaction statuses does not match the expected number.

    Notes:
        - This function assumes that the transaction statuses are ordered as well as the logs within each receipt.
    """
def sadflow_open(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Handles the sadflow for the init open position state.
    Calls the appropriate function based on the status of the actions.
    """
def sadflow_open_retry(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Handles the basic retry sadflow.
    """
def sadflow_open_partial_retry(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Handles the complex partial retry sadflow.

    The Prepare Action sends: actions=[action_approve0, action_approve1, action_open]
    - Failure #1: One of the Approves failed -> We retry the same state as is.
    - Failure #2: Open failed -> We check the revert reason.
                              -> For now we simply retry the same state as is (updating values),
                                 because we don't care too much double approving.
                  Known revert reasons:
                    - STF: Retry the same state for now.
                    - Slippage: Retry the same state for now.
    """
