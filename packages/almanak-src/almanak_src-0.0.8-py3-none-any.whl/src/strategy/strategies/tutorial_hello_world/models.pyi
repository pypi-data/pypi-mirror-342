from enum import Enum
from src.almanak_library.enums import Chain as Chain, Network as Network, Protocol as Protocol
from src.strategy.models import PersistentStateBase as PersistentStateBase, StrategyConfigBase as StrategyConfigBase

class State(Enum):
    """Enum representing the state of the strategy."""
    INITIALIZATION = 'INITIALIZATION'
    DISPLAY_MESSAGE = 'DISPLAY_MESSAGE'
    COMPLETED = 'COMPLETED'
    TEARDOWN = 'TEARDOWN'
    TERMINATED = 'TERMINATED'

class SubState(Enum):
    """Enum representing the substates of some of the strategy states. A state machine within a state machine."""
    NO_SUBSTATE = 'NO_SUBSTATE'

class PersistentState(PersistentStateBase):
    current_state: State
    current_substate: SubState
    last_message: str

class StrategyConfig(StrategyConfigBase):
    id: str
    network: Network
    chain: Chain
    protocol: Protocol
    initiate_teardown: bool
    pause_strategy: bool
    message: str
