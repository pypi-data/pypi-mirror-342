from enum import Enum
from pydantic import BaseModel
from typing import Any
from uuid import UUID

class Mode(Enum):
    EXECUTION = 'EXECUTION'
    RECOMMENDATIONS = 'RECOMMENDATIONS'

class InternalFlowStatus(Enum):
    """Internal flow allowing the state to prepare its actions, validate them and handle its own sadflow."""
    PREPARING_ACTION = 'PREPARING_ACTION'
    VALIDATING_ACTION = 'VALIDATING_ACTION'
    SADFLOW_ACTION = 'SADFLOW_ACTION'

class StateBase(Enum):
    INITIALIZATION = 'INITIALIZATION'
    COMPLETED = 'COMPLETED'
    TEARDOWN = 'TEARDOWN'
    TERMINATED = 'TERMINATED'

class SubStateBase(Enum):
    NO_SUBSTATE = 'NO_SUBSTATE'

class PersistentStateBase(BaseModel):
    current_state: StateBase
    current_flowstatus: InternalFlowStatus
    current_actions: list[UUID]
    initialized: bool
    completed: bool

class StrategyConfigBase(BaseModel):
    cosigner: dict[str, Any] | None
