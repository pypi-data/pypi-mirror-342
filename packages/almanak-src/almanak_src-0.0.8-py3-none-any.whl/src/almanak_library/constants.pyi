from enum import Enum
from src.almanak_library.enums import Chain as Chain, Network as Network

class MessageStatus(Enum):
    MESSAGE_SUCCESS = 'MESSAGE_SUCCESS'
    MESSAGE_ERROR = 'MESSAGE_ERROR'

class MainStatus(Enum):
    MAIN_SUCCESS = 'MAIN_SUCCESS'
    MAIN_ERROR = 'MAIN_ERROR'
    MAIN_REBALANCE = 'MAIN_REBALANCE'
    MAIN_PAUSE = 'MAIN_PAUSE'
    MAIN_TEARDOWN = 'MAIN_TEARDOWN'

class CustomSimulationStatus(Enum):
    COMPLETED_VIA_LOGS = 'COMPLETED_VIA_LOGS'
    NOT_COMPLETED_VIA_LOGS = 'NOT_COMPLETED_VIA_LOGS'

class RebalancingStatus(Enum):
    REBALANCING_REQUIRED = 'REBALANCING_REQUIRED'
    RUNNING_REBALANCING_FOR_OPTICS = 'RUNNING_REBALANCING_FOR_OPTICS'
    NO_POSITION = 'NO_POSITION'

class TriggerEvents(Enum):
    TELEGRAM_MESSAGE_SENT = 'TELEGRAM_MESSAGE_SENT'
    SIMULATE_ON_NO_POSITION = 'SIMULATE_ON_NO_POSITION'

ETH_ADDRESS: str

def get_address_by_chain_and_network(chain: Chain, network: Network, contract_name: str): ...

PROD_PROJECT_ID: str
STAGING_PROJECT_ID: str
