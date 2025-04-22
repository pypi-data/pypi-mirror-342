from _typeshed import Incomplete
from enum import Enum
from pydantic import BaseModel
from src.utils.config import Config as Config

IS_AGENT_DEPLOYMENT: Incomplete
MACHINE_FILENAME: str
storage_client: Incomplete

class AgentMachineStatus(Enum):
    SUCCESS = 'SUCCESS'

class AgentMachineState(Enum):
    RUNNING = 'RUNNING'
    CLEAN_PAUSE = 'CLEAN_PAUSE'
    CLEAN_TEARDOWN = 'CLEAN_TEARDOWN'
    MAX_RETRIES_REACHED = 'MAX_RETRIES_REACHED'

class AgentMachineSchema(BaseModel):
    status: AgentMachineStatus
    state: AgentMachineState
    timestamp: str
    message: str | None
    metadata: dict | None

def build_agent_machine_json(agent_machine_state: AgentMachineState, message: str | None = None) -> str: ...
def upload_agent_machine_file(agent_machine_status: AgentMachineStatus, message: str | None = None): ...
