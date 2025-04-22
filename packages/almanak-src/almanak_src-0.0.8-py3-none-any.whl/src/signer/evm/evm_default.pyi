from _typeshed import Incomplete
from enum import Enum
from hexbytes import HexBytes as HexBytes
from pathlib import Path as Path
from pydantic import BaseModel
from src.almanak_library.enums import Chain as Chain, ExecutionStatus as ExecutionStatus, Network as Network, TransactionType as TransactionType
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.models.transaction import Transaction as Transaction
from src.signer.evm.agent_utils import get_eoa_address_for_safe_wallet as get_eoa_address_for_safe_wallet
from src.signer.interfaces import CoSignerInterface as CoSignerInterface
from src.signer.utils import get_keyfile as get_keyfile, get_secret as get_secret
from src.utils.config import Config as Config
from src.utils.utils import get_web3_by_network_and_chain as get_web3_by_network_and_chain, is_EVM_compatible_chain as is_EVM_compatible_chain
from typing import Any
from web3 import Web3 as Web3

GAS_BUFFER: float
DEBUG: Incomplete
IS_AGENT_DEPLOYMENT: Incomplete
SIGNER_SERVICE_ENDPOINT_ROOT: Incomplete
PLATFORM_TRANSACTIONS_GCS_BUCKET: Incomplete
SIGNER_SERVICE_JWT: Incomplete
ZODIAC_ROLE_CONTRACT_ADDRESS: Incomplete

def get_private_key_envs(): ...

account: Incomplete
ZODIAC_EXEC_TRANSACTION_WITH_ROLE_ABI: Incomplete

class Hash(BaseModel):
    hash: str
    def hex(self): ...

class RawTransaction(BaseModel):
    rawTransaction: str
    def hex(self): ...

class SignedTransaction(BaseModel):
    hash: Hash
    rawTransaction: RawTransaction

class SignerEVMDefault(CoSignerInterface):
    def __init__(self) -> None: ...
    def sign_transactions(self, action_bundle: ActionBundle, cosigning_config: dict[str, Any]) -> ActionBundle:
        """
        Sign the transactions in the action bundle
        """

class SignerEVMAgent(SignerEVMDefault):
    zodiac_role_name: str
    zodiac_role_key: Incomplete
    def __init__(self) -> None: ...
    class ZodiacRoleOperation(Enum):
        Call = 0
        DelegateCall = 1
    @staticmethod
    def to_bytes32_bytes(string: str) -> bytes: ...
    @staticmethod
    def get_txn_hash_from_txn(signed_transaction: str, web3: Web3) -> str: ...
