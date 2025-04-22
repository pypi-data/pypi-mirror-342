from _typeshed import Incomplete
from src.almanak_library.enums import ExecutionStatus as ExecutionStatus
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.profiler.time_block import ProfileType as ProfileType
from src.almanak_library.profiler.utils import time_block as time_block
from src.executer.execution_manager import ExecutionManager as ExecutionManager
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger
from src.utils.utils import get_web3_by_network_and_chain as get_web3_by_network_and_chain, retry_on_exception as retry_on_exception, upload_action_bundle_to_storage as upload_action_bundle_to_storage

logger: Incomplete
EVM_TIMEOUT_MINIMUM: int
EVM_TIMEOUT_BUFFER: int
CHAINBOUND_ETHEREUM_ECHO_URL: str
MAX_RETRIES_ON_CHAINBOUND_SEND: int
TIME_SLEEP_BETWEEN_CHAINBOUND_REQUESTS: int

def send_bundle_chainbound(action_bundle: ActionBundle, payload: dict, headers: dict, replacement_id: str): ...
def cancel_bundle_chainbound(replacement_id: str, mev_builders: list[str] | None = None) -> bool:
    """Using this as fallback to timeout on the request"""
def execute_transaction_bundle_ethereum_mainnet(action_bundle: ActionBundle, execution_manager: ExecutionManager) -> ActionBundle: ...
def get_executed_bundle_status_ethereum_mainnet(action_bundle: ActionBundle, execution_manager: ExecutionManager) -> ActionBundle: ...
