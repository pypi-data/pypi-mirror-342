from _typeshed import Incomplete
from src.strategy.strategies.dynamic_lp.metrics import log_rebalance_trigger_metrics as log_rebalance_trigger_metrics
from src.strategy.strategies.dynamic_lp.strategy import StrategyDynamicLP as StrategyDynamicLP
from src.strategy.utils.price_volatility import get_price_and_volatility as get_price_and_volatility
from src.strategy.utils.utils import convert_time_window as convert_time_window
from src.utils.config import Config as Config

DEBUG_ALWAYS_REBALANCE: Incomplete
PRODUCTION_MODE: Incomplete

def check_for_rebalance(strat: StrategyDynamicLP) -> None:
    """
    Evaluates the need for rebalancing the strategy based on market conditions and strategy parameters.

    This method checks if the current position is out of the rebalance soft bounds or if a rebalance is due
    based on the set rebalance interval (frequency). It sets the strategy's next state accordingly, either to close the current
    position for rebalancing or to mark the completion if no rebalance is needed. A grace period can be used to
    avoid frequent rebalances when the bounds are quickly exceeded but the price is mean reverting.

    Raises:
        ValueError: If a rebalance is needed but there are no positions to rebalance, which is currently
                    not supported by the strategy.

    Returns:
        None: No actions are required in this state.
    """
