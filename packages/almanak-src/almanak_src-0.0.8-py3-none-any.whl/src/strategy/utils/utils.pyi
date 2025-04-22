from decimal import Decimal
from enum import Enum
from src.almanak_library.enums import ActionType as ActionType, Protocol as Protocol
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.params import ApproveParams as ApproveParams

class DataSource(Enum):
    BINANCE = 'BINANCE'
    COINGECKO = 'COINGECKO'
    COINGECKO_DEX = 'COINGECKO_DEX'

class DataFormat(Enum):
    OHLCV = 'OHLCV'
    OHLC = 'OHLC'
    CLOSE = 'CLOSE'
    HIGH = 'HIGH'
    LOW = 'LOW'
    OPEN = 'OPEN'

class ETHNativeChains(Enum):
    ETHEREUM = 'ETHEREUM'
    BASE = 'BASE'
    OPTIMISM = 'OPTIMISM'
    ARBITRUM = 'ARBITRUM'

def convert_time_window(window: float | int, input_granularity: str, output_granularity: str): ...
def to_readable(amount: int, token_decimals: int) -> Decimal:
    """
    Converts integer amount to a readable Decimal format based on the token's decimals.

    :param amount: The raw integer amount.
    :param token_decimals: The number of decimal places for the token.
    :return: The amount in a more readable Decimal format.
    """
def create_approve_1token_action(token_address: str, from_address: str, spender_address: str, amount: int, protocol: Protocol) -> Action:
    """
    Creates the Action to approve a specified amount of a token for use by another address.

    Args:
        token_address (str): The blockchain address of the token to be approved.
        from_address (str): The address of the token holder who is giving the approval.
        spender_address (str): The address of the contract or account that will be allowed to spend the tokens.
        amount (int): The amount of tokens to be approved, typically specified in the smallest unit of the token (e.g., wei).

    Returns:
        Action: Approve Action.
    """
def create_approve_2tokens_actions(token0_address: str, token1_address: str, from_address: str, spender_address: str, amount0: int, amount1: int, protocol: Protocol) -> tuple[Action, Action]:
    """
    Creates approval actions for two different tokens to allow a designated spender to utilize them on behalf of the sender.

    This method generates two separate approval actions required for operations such as providing liquidity
    or executing trades where access to more than one type of token is necessary. This method is crucial for
    ensuring that smart contracts or other addresses are authorized to manage tokens under predefined limits.

    Args:
        token0_address (str): The blockchain address of the first token to be approved.
        token1_address (str): The blockchain address of the second token to be approved.
        from_address (str): The address of the token holder giving the approval.
        spender_address (str): The address of the entity that is being authorized to use the tokens.
        amount0 (int): The amount of the first token that the spender is authorized to use.
        amount1 (int): The amount of the second token that the spender is authorized to use.

    Returns:
        Tuple[Action, Action]: A tuple containing the approval actions for both token0 and token1.
    """
def get_action_by_type(actions, action_type) -> list[Action]:
    """
    Retrieves an action from a list of actions based on the specified action type.
    """
