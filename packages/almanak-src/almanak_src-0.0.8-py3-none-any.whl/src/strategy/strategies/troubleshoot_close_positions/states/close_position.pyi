from ..strategy import StrategyTroubleshootClosePositions as StrategyTroubleshootClosePositions
from src.almanak_library.enums import ActionType as ActionType, ExecutionStatus as ExecutionStatus
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.models.params import ClosePositionParams as ClosePositionParams
from time import sleep as sleep

def close_position(strat: StrategyTroubleshootClosePositions) -> ActionBundle:
    """
    Closes the current liquidity position in the pool.

    This function constructs an action to close the liquidity position identified by `position_id`.
    The liquidity and the fees are collected, and the NFT position is burned and 100% of these assets will
    be used to open the next position. It uses the Close Position Multicall Action.

    Returns:
        ActionBundle: An action bundle with the close position action (using the multicall action).
    """
def prepare_close_position(strat: StrategyTroubleshootClosePositions) -> ActionBundle:
    """
    Prepares the close position actions.

    Returns:
        ActionBundle: An action bundle with the close position action (using the multicall action).
    """
def validate_close_position(strat: StrategyTroubleshootClosePositions) -> bool:
    """
    Validates the close position actions and retrieves the amounts from closing the position (liquidity + fees),
    using transaction receipts. It loads the transaction statuses from the executioner and processes them.

    Returns:
        bool: True if the close position actions were successful and the amounts were retrieved correctly.

    Notes:
        The only possible ExecutionStatus at this point is ExecutionStatus.SUCCESS
        otherwise should be in sadflow redoing the actions.
    """
def sadflow_close_position(strat: StrategyTroubleshootClosePositions) -> ActionBundle:
    """
    Handles the sadflow for the close position state.
    Calls the appropriate function based on the status of the actions.
    """
def sadflow_retry(strat: StrategyTroubleshootClosePositions) -> ActionBundle:
    """
    Handles the basic retry sadflow.
    """
def sadflow_partial_retry(strat: StrategyTroubleshootClosePositions) -> ActionBundle:
    """
    Handles the complex partial retry sadflow.

    Close position with Multicall has no partial sadflow, it's all or nothing.
    """
