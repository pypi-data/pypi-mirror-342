from enum import Enum
from src.almanak_library.enums import Chain as Chain, Network as Network, Protocol as Protocol
from src.strategy.models import InternalFlowStatus as InternalFlowStatus, PersistentStateBase as PersistentStateBase, StrategyConfigBase as StrategyConfigBase
from uuid import UUID

class State(Enum):
    """Enum representing the state of the strategy."""
    INITIALIZATION = 'INITIALIZATION'
    CHECK_POSITIONS = 'CHECK_POSITIONS'
    CLOSE_POSITION = 'CLOSE_POSITION'
    COMPLETED = 'COMPLETED'
    TEARDOWN = 'TEARDOWN'
    TERMINATED = 'TERMINATED'

class SubState(Enum):
    """Enum representing the substates of some of the strategy states. A state machine within a state machine."""
    NO_SUBSTATE = 'NO_SUBSTATE'

class PersistentState(PersistentStateBase):
    current_state: State
    current_substate: SubState
    current_flowstatus: InternalFlowStatus
    current_actions: list[UUID]
    sadflow_counter: int
    sadflow_actions: list[UUID]
    not_included_counter: int
    position_to_close: int

class StrategyConfig(StrategyConfigBase):
    id: str
    network: Network
    chain: Chain
    protocol: Protocol
    wallet_address: str
    specific_positions: list[int]
    specific_pools: list[str]
