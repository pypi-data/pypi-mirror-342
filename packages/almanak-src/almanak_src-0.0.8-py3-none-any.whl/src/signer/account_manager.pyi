from _typeshed import Incomplete
from src.almanak_library.enums import CoSigners as CoSigners, ExecutionStatus as ExecutionStatus
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.signer.evm.evm_default import SignerEVMAgent as SignerEVMAgent, SignerEVMDefault as SignerEVMDefault
from src.signer.evm.evm_eulith import CoSignerEVMEulith as CoSignerEVMEulith
from src.utils.config import Config as Config
from src.utils.utils import is_EVM_compatible_chain as is_EVM_compatible_chain

IS_AGENT_DEPLOYMENT: Incomplete

class AccountManager:
    def __init__(self) -> None: ...
    def sign_transactions(self, action_bundle: ActionBundle) -> ActionBundle:
        """
        Sign the transactions in the action bundle
        """
