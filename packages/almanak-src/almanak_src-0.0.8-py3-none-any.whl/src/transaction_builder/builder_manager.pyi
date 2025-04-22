from _typeshed import Incomplete
from ast import parse as parse
from pprint import pprint as pprint
from src.almanak_library.custom_exceptions import SimulationError as SimulationError
from src.almanak_library.enums import ActionType as ActionType, Chain as Chain, CoSigners as CoSigners, ExecutionStatus as ExecutionStatus, Network as Network, Protocol as Protocol, SwapSide as SwapSide, TransactionType as TransactionType
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.models.params import ApproveParams as ApproveParams, ClosePositionParams as ClosePositionParams, OpenPositionParams as OpenPositionParams, SwapParams as SwapParams, TransferParams as TransferParams, UnwrapParams as UnwrapParams, WrapParams as WrapParams
from src.almanak_library.models.sdk import ISDK as ISDK
from src.almanak_library.models.transaction import Transaction as Transaction
from src.utils.config import Config as Config
from src.utils.utils import get_logger as get_logger, get_protocol_sdk as get_protocol_sdk, get_web3_by_network_and_chain as get_web3_by_network_and_chain
from web3 import Web3 as Web3

IS_AGENT_DEPLOYMENT: Incomplete
logger: Incomplete

class TransactionManager:
    supported_actions: Incomplete
    params_classes: Incomplete
    chain_protocol_dict: Incomplete
    chain_network_dict: Incomplete
    GAS_BUFFER: float
    ARBITRUM_ALCHEMY_GAS_BUFFER: float
    BASE_GAS_BUFFER: float
    def __init__(self) -> None: ...
    def build_transactions_from_action_bundle(self, action_bundle: ActionBundle, block_identifier: Incomplete | None = None) -> ActionBundle:
        """
        this function executes multiple actions in a single bundle.
        It uses simulate execution bundle to build the transactions, estimate the gas,
        so that the transactions that depends on a previous one can be simulated.

        # NOTE: actions within the bundle should have the same network and chain.
        """
    def parse_alchemy_result(self, results) -> None:
        """
        Parses the Alchemy simulation results to extract and log error details.

        This function handles its own exceptions to prevent them from propagating
        and stopping the program execution.

        Parameters:
        - results (list): The list of simulation results from Alchemy.
        """
    def handle_transfer(self, params: TransferParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        Handles the process of transferring tokens from one address to another.
        """
    def handle_wrap(self, params: WrapParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        the standard ERC20 deposit function for WETH does not inherently support a deadline parameter
        """
    def handle_unwrap(self, params: UnwrapParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        the standard ERC20 withdraw function for Wrap Token does not inherently support a deadline parameter
        """
    def handle_approve(self, params: ApproveParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        the ERC20 approve function itself does not natively support a deadline parameter
        """
    def handle_swap(self, params: SwapParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]: ...
    def handle_open_position(self, params: OpenPositionParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        Handles the process of opening a new liquidity position.
        It is important to note that you need to call the approve method for both tokens involved
        in the liquidity position before calling this function. The approve method should authorize the position manager contract
        to spend the specified amount of tokens on behalf of the user's address.
        """
    def handle_close_position(self, params: ClosePositionParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        # collect and burn does noth have a deadline on the smart contract level
        """
    def handle_close_position_multicall(self, params: ClosePositionParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]: ...
