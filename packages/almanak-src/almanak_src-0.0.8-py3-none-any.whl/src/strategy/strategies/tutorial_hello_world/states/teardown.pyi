from ..strategy import StrategyTemplateHelloWorld as StrategyTemplateHelloWorld
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle

def teardown(strat: StrategyTemplateHelloWorld) -> ActionBundle:
    """
    Concludes the strategy by closing any active positions and preparing the system for a reset or shutdown.
    Leaves the system in a state where it can be cleanly initialized again.

    Returns:
        ActionBundle | None: An action bundle with the teardown actions.
    """
