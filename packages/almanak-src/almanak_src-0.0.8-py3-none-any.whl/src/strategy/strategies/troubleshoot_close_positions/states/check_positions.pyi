from ..strategy import StrategyTroubleshootClosePositions as StrategyTroubleshootClosePositions
from pprint import pprint as pprint
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from time import sleep as sleep

def check_positions(strat: StrategyTroubleshootClosePositions) -> ActionBundle:
    """
    Checks positions and selects one to close based on config.
    This function is recalled until all relevant positions are closed.
    """
