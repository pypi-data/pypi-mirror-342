from ..strategy import StrategyTemplateHelloWorld as StrategyTemplateHelloWorld
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle

def initialization(strat: StrategyTemplateHelloWorld) -> ActionBundle:
    """
    Initializes the strategy by preparing assets and opening positions.

    The initialization process may involve swapping assets, wrapping ETH, and opening liquidity positions.
    It operates in several substates to manage the sequence of actions.

    Returns:
        ActionBundle: An action bundle representing the actions required to initialize
        the strategy, or None if no actions are required.

    Notes:
        - This method should only be called at the start of the strategy lifecycle.
        - The process is divided into substates to handle complex initialization steps.
    """
