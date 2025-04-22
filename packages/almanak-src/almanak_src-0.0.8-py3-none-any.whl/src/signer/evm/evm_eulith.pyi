from _typeshed import Incomplete
from src.almanak_library.enums import Chain as Chain, ExecutionStatus as ExecutionStatus, Network as Network
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.signer.evm.evm_default import SignerEVMDefault as SignerEVMDefault
from src.utils.config import Config as Config
from src.utils.utils import get_web3_by_network_and_chain as get_web3_by_network_and_chain
from typing import Any

DEBUG: Incomplete
GAS_BUFFER: float

class CoSignerEVMEulith(SignerEVMDefault):
    eulith_imports_loaded: bool
    EulithWeb3: Incomplete
    EulithRpcException: Incomplete
    LocalSigner: Incomplete
    construct_signing_middleware: Incomplete
    def __init__(self) -> None: ...
    def sign_transactions(self, action_bundle: ActionBundle, cosigning_config: dict[str, Any]) -> ActionBundle:
        """
        Overridden method to sign transactions with specific logic for Eulith.
        """
