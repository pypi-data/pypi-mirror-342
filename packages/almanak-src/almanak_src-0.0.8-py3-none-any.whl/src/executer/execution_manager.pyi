from _typeshed import Incomplete
from src.almanak_library.enums import Chain as Chain, ExecutionStatus as ExecutionStatus, Network as Network
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.models.transaction import Transaction as Transaction
from src.almanak_library.receipt_parser.receipt_parser_manager import ReceiptParserManager as ReceiptParserManager
from src.executer.interfaces import ExecutionEthereumMainnet as ExecutionEthereumMainnet, ExecutionEthereumPublic as ExecutionEthereumPublic, ExecutionInterface as ExecutionInterface
from src.utils.logger import get_logger as get_logger
from src.utils.utils import retry_on_exception as retry_on_exception
from web3 import Web3 as Web3

logger: Incomplete

class ExecutionManager:
    executor_map: Incomplete
    receipt_parser_manager: Incomplete
    def __init__(self) -> None: ...
    def get_revert_reason(self, web3, tx_hash): ...
    def wait_for_transaction_receipt(self, web3: Web3, tx_hash: str, timeout: int) -> dict | None: ...
    def execute_transaction_bundle(self, action_bundle: ActionBundle) -> ActionBundle: ...
    def get_executed_bundle_status(self, action_bundle: ActionBundle) -> ActionBundle: ...
