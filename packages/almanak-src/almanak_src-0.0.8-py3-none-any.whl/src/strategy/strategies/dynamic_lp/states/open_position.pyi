from src.almanak_library.enums import ActionType as ActionType, ExecutionStatus as ExecutionStatus, TransactionType as TransactionType
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.models.params import OpenPositionParams as OpenPositionParams
from src.strategy.strategies.dynamic_lp.strategy import StrategyDynamicLP as StrategyDynamicLP
from src.strategy.utils.price_volatility import get_current_price_and_volatility as get_current_price_and_volatility
from src.strategy.utils.utils import create_approve_2tokens_actions as create_approve_2tokens_actions, to_readable as to_readable

def open_position(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Opens a new liquidity position based on the current market conditions and strategy settings.

    This function calculates the amounts to be used for the new position from the tokens available
    after close & swaps then determines the price bounds for the position based on current market price
    and strategy-defined volatility.

    Args:
        strat (StrategyDynamicLP): The Strategy instance.

    Returns:
        ActionBundle: A bundle of actions including token approvals and the open/mint transaction.

    Notes:
        - Bounds are in human readable prices, not in ticks. The conversion is done in the SDK.

    TODO: Need to support for other model. Currently implicitly assuming volatility model.
    """
def prepare_open_position(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Prepares the open position actions.

    Returns:
        ActionBundle: A bundle of actions including token approvals and the open/mint transaction.
    """
def validate_open_position(strat: StrategyDynamicLP) -> bool:
    """
    Validates the open position actions and retrieves the executed amounts in the execution details.

    Returns:
        bool: True if the open position actions were successful and the amounts were retrieved correctly
              and can move to the next state.
    """
def sadflow_open_position(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Handles the sadflow for the open position state.
    Calls the appropriate function based on the status of the actions.
    """
def sadflow_retry(strat: StrategyDynamicLP) -> ActionBundle:
    """
    Handles the basic retry sadflow.
    """
def sadflow_partial_retry(strat: StrategyDynamicLP) -> ActionBundle:
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
def calculate_position(strat: StrategyDynamicLP, include_last_swap_amounts: bool, use_specified_amounts: bool = False, amount0: int = 0, amount1: int = 0, verbose: bool = True) -> dict:
    """
    Calculate the LP Position based on given parameters.

    Args:
        strat (StrategyDynamicLP): The strategy instance containing relevant configuration and models.
        include_last_swap_amounts (bool): Whether to include the amounts from the last swap when calculating available capital.
        use_specified_amounts (bool, optional): If True, use the specified `amount0` and `amount1` instead of calculating based on available capital. Defaults to False.
        amount0 (int, optional): The specified amount of token0 to use for the position. Ignored if `use_specified_amounts` is False. Defaults to 0.
        amount1 (int, optional): The specified amount of token1 to use for the position. Ignored if `use_specified_amounts` is False. Defaults to 0.
        verbose (bool, optional): If True, prints additional debug information during the calculation. Defaults to True.

    Returns:
        dict: A dictionary containing the calculated position details:
            - 'amounts': Tuple of the calculated amounts for token0 and token1.
            - 'range': Tuple of the calculated price range (price_lower, price_upper).
            - 'unallocated': Tuple of the unallocated amounts for token0 and token1 vs position calculation.

    Raises:
        ValueError: If there is an issue with price bounds, invalid specified amounts, or any errors during the calculation process.
        NotImplementedError: If the strategy model other than volatility is requested.

    Example:
        result = calculate_position(strat, include_last_swap
    """
