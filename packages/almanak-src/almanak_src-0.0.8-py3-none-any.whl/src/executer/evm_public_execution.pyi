from _typeshed import Incomplete
from src.almanak_library.enums import ExecutionStatus as ExecutionStatus
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.profiler.time_block import ProfileType as ProfileType
from src.almanak_library.profiler.utils import time_block as time_block
from src.executer.execution_manager import ExecutionManager as ExecutionManager
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger
from src.utils.utils import get_web3_by_network_and_chain as get_web3_by_network_and_chain, retry_get_block as retry_get_block, upload_action_bundle_to_storage as upload_action_bundle_to_storage

logger: Incomplete
EVM_TIMEOUT_MINIMUM: int
DEBUG: Incomplete
EVM_TIMEOUT_BUFFER: int
passable_send_errors: Incomplete

def passable_send_exception(e: Exception):
    """
    Example error message:
    `{
    'code': -32000,
    'message': 'max fee per gas less than block base fee: address 0x6e529B268705545Ffb94bf4E6d53AB68B90091E7, maxFeePerGas: 29382100 baseFee: 30058000'
    }`
    """
def execute_transaction_bundle_evm_public(action_bundle: ActionBundle, execution_manager: ExecutionManager) -> ActionBundle:
    """
    NOTE: Does not guarantee all or nothing execution of the action bundle.
    Can have any number of transactions executed serially.
    The current design returns at the first non-successful transaction.
    """
def get_executed_bundle_status_evm_public(action_bundle: ActionBundle, execution_manager: ExecutionManager) -> ActionBundle:
    """
    This is used to parse the receipt on an unknown status. Once the status is not unknown,
    the strategy can continue from whatever state is found.
    """
