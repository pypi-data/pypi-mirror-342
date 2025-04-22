import uuid
from src.almanak_library.enums import Chain as Chain, CoSigners as CoSigners, ExecutionStatus as ExecutionStatus, Network as Network, Protocol as Protocol
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.models.receipt import Receipt as Receipt
from src.almanak_library.receipt_parser.i_receipt_parser import IReceiptParser as IReceiptParser
from src.almanak_library.receipt_parser.uniswap_v3_receipt import ReceiptParserUniswapV3 as ReceiptParserUniswapV3
from src.utils.utils import get_web3_by_network_and_chain as get_web3_by_network_and_chain, retry_get_block as retry_get_block
from typing import Any

class ReceiptParserManager:
    parse_map: dict[tuple[Protocol, Network, Chain], IReceiptParser]
    def __init__(self) -> None: ...
    def parse_receipts(self, action_bundle: ActionBundle, receipts: list[dict[str, Any]]) -> list[Receipt]: ...
    def should_parse_receipt_for_action(self, action_bundle: ActionBundle, action_id: uuid.UUID) -> bool:
        """
        Only parse receipt for action if all transactions are successful.
        """
