from _typeshed import Incomplete
from src.almanak_library.enums import Chain as Chain, Network as Network
from src.strategy.strategy_base import Strategy as Strategy
from src.utils.utils import get_web3_by_network_and_chain as get_web3_by_network_and_chain

STRATEGY_DIRECTORY: str

class StrategyFactory:
    strategies: Incomplete
    @staticmethod
    def register_strategies() -> None: ...
    @staticmethod
    def create_strategy(strategy_name, parameters): ...
    @staticmethod
    def get_strategies(): ...

def get_parameters_from_config(config: dict, strategy_id: str, verbose: bool = True) -> tuple[str, dict]: ...
def create_strategy_from_config(config: dict, strategy_id: str) -> Strategy:
    """
    Extracts shared and specific strategy configuration, merges shared parameters with specific parameters
    for the strategy corresponding to the strategy_id received, and create the strategy instance using the StrategyFactory.

    Returns:
       Strategy instance (or None if the strategy_id is not found).
    """
def get_strategy_ids_from_config(config: dict) -> list[str]: ...
