from _typeshed import Incomplete
from hexbytes import HexBytes as HexBytes
from src.almanak_library.enums import ActionType as ActionType, Chain as Chain, ExecutionStatus as ExecutionStatus, Network as Network, Protocol as Protocol, TransactionType as TransactionType
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.receipt import ApproveReceipt as ApproveReceipt, ClosePositionReceipt as ClosePositionReceipt, OpenPositionReceipt as OpenPositionReceipt, Receipt as Receipt, SwapReceipt as SwapReceipt, UnwrapReceipt as UnwrapReceipt, WrapReceipt as WrapReceipt
from src.almanak_library.models.sdk import ISDK as ISDK
from src.almanak_library.receipt_parser.i_receipt_parser import IReceiptParser as IReceiptParser
from src.transaction_builder.protocols.uniswap_v3.uniswap_v3_sdk import UniswapV3SDK as UniswapV3SDK
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger
from src.utils.utils import get_protocol_sdk as get_protocol_sdk
from typing import Any

DEBUG: Incomplete
logger: Incomplete

class ReceiptParserUniswapV3(IReceiptParser):
    """
    identify log based on topic[0]
    find the receipt based on the transaction hash in the log
    link action and receipt based on the action id
    """
    action_map: Incomplete
    EVENT_SIGNATURE_BYTES: Incomplete
    protocol: Incomplete
    network: Incomplete
    chain: Incomplete
    sdk: Incomplete
    def __init__(self, protocol: Protocol, network: Network, chain: Chain) -> None: ...
    def initialize_sdk(self) -> ISDK: ...
    @staticmethod
    def find_logs_from_signature_bytes(logs: list[dict], event_signature_bytes: str) -> list:
        """
        Helper function to filter logs based on the event signature bytes.
        Returns a list of logs that match the event signature bytes. In most cases, only 1 log is expected.
        """
    @staticmethod
    def filter_logs_by_action(logs: list[dict], action: Action) -> list: ...
    def flatten_logs(self, receipts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Flatten the logs from all receipts into a single list.
        """
    def find_receipt_by_transaction_hash(self, transaction_hash: HexBytes, receipts: list[dict[str, Any]]) -> dict[str, Any] | None:
        """
        Find a receipt that matches the given transactionHash from a list of receipts.

        Args:
            transaction_hash (str): The transaction hash to search for.
            receipts (List[Dict[str, Any]]): The list of receipts to search within.

        Returns:
            Optional[Dict[str, Any]]: The matching receipt if found, otherwise None.
        """
    def unwrap_parser(self, action: Action, chain: Chain, transfer_offset: int, multicall_action: bool, receipts: list[dict[str, Any]]) -> Receipt | None: ...
    def wrap_parser(self, action: Action, chain: Chain, transfer_offset: int, mulitcall_action: bool, receipts: list[dict[str, Any]]) -> Receipt | None: ...
    def approve_parser(self, action: Action, chain: Chain, transfer_offset: int, multicall_action: bool, receipts: list[dict[str, Any]]) -> Receipt | None: ...
    def swap_parser(self, action: Action, chain: Chain, transfer_offset: int, multicall_action: bool, receipts: list[dict[str, Any]]) -> Receipt | None:
        """
        Validates the swap actions and retrieves the executed amounts using transaction receipts.

        Transactions:
            TX: Swap
                - Log #0: Transfer Pool -> Recipient
                - Log #1: Transfer Recipient -> Pool
        """
    def open_position_parser(self, action: Action, chain: Chain, offset: int, multicall_action: bool, receipts: list[dict[str, Any]]) -> Receipt | None:
        """
        Validates the open position actions and retrieves the executed amounts using transaction receipts.

        Transactions:
            TX: Open Position (mint NFT)
                - Log #0: Transfer (Token0)
                - Log #1: Transfer (Token1)
                - Log #2: Mint (Pool)
                - Log #3: Transfer (Mint NFT)
                - Log #4: IncreaseLiquidity (NFT)
        """
    def close_position_parser_multicall(self, action: Action, chain: Chain, transfer_offset: int, multicall_action: bool, receipts: list[dict[str, Any]]) -> Receipt | None:
        """
        Parses the amounts from closing the position (liquidity + fees) using a *multicall* transaction receipt.

        Transaction logs:
        - Log #0: Burn
        - Log #1: DecreaseLiquidity (NFT)
        - Log #2: Transfer (token0 from UV3 Pool to LP)
        - Log #3: Transfer (token1 from UV3 Pool to LP)
        - Log #4: Collect (Pool)
        - Log #5: Collect (NFT)
        - Log #6: Transfer (to lp)
        - Log #7: Transfer (to lp)

        example: https://etherscan.io/tx/0xb2ed92c210ae8baa186555cc72d719d164acd3e9c74b94bae1abec0c73032220#eventlog
        """
