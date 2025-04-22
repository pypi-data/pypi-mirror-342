from _typeshed import Incomplete
from src.almanak_library.enums import Chain as Chain, Network as Network, Protocol as Protocol
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.models.sdk import ISDK as ISDK
from src.almanak_library.sdk_registry import sdk_registry as sdk_registry
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger
from web3 import Web3

cached_w3_clients: dict[str, Web3]
cached_sdk_clients: dict[tuple[Protocol, Network, Chain], ISDK]
logger: Incomplete
NUM_RETRIES_WARN: int
IS_AGENT_DEPLOYMENT: Incomplete
DEBUG: Incomplete
storage_client: Incomplete
PLATFORM_TRANSACTIONS_GCS_BUCKET: Incomplete
STORAGE_DIR: Incomplete

def is_staging_env() -> bool: ...
def set_on_test_mode(test_value): ...
def get_node_provider_by_network_and_chain(network: Network, chain: Chain):
    """
    Return the node provider for the given network and chain
    """
def get_web3_by_network_and_chain(network: Network, chain: Chain) -> Web3:
    """
    Create a web3 client for the user_address and cache it. Recreates if not connected.
    """
def is_EVM_compatible_chain(chain: Chain) -> bool: ...
def serialize_timestamp(timestamp: float) -> str:
    """Convert a Unix timestamp to a human-readable string."""
def deserialize_timestamp(timestamp_str: str) -> float:
    """Convert a human-readable string to a Unix timestamp."""
def retry_on_exception_for_download(max_retries: int = 3, delay: int = 2):
    """
    Retry decorator specifically for the download_action_bundle_from_storage function.
    It returns None if NotFound exception persists after all retries and raises
    any other exception immediately or after retries.
    """
def retry_on_exception(max_retries: int = 3, delay: int = 2, exceptions=..., return_value: Incomplete | None = None):
    """
    Retry decorator for functions that may raise exceptions.
    This is a simple retry mechanism.
    It is used to prevent the service from crashing due to transient errors.
    """
def upload_transaction_for_agent_gcs(blob_str: str, raw_transaction: str): ...
def upload_transaction_for_agent(blob_str: str, raw_transaction: str): ...
def upload_transactions_for_agent(action_bundle: ActionBundle): ...
def upload_action_bundle_to_storage(action_bundle: ActionBundle): ...
def upload_action_bundle_to_storage_local(action_bundle: ActionBundle): ...
def upload_action_bundle_to_storage_gcs(action_bundle: ActionBundle):
    """
    Writes in a GCS file to update the status of a given Action.
    The filename is the Action UUID and the content is pickled for simplicity.
    The Executioner is the only one writing in this/these files, the other services are only reading them.

    Raises:
        FileNotFoundError: If the configuration file is not found at the specified path.
        ValueError: If there is an error decoding JSON from the configuration file.
        EnvironmentError: If required environment variables are not set.
        PermissionsError: If there are insufficient permissions to access the file.
        TimeoutError: If the request to download the configuration file times out.
        GoogleAPICallError: For network-related errors or issues on the backend from Google Cloud services.
    """
def download_action_bundle_from_storage(gcs_bucket_name, client_name, deployment_name, strategy_id, action_id, object_cls): ...
def download_action_bundle_from_storage_local(strategy_id, action_id, object_cls): ...
def download_action_bundle_from_storage_gcs(gcs_bucket_name, client_name, deployment_name, strategy_id, action_id, object_cls): ...
def get_protocol_sdk(protocol: Protocol, network: Network, chain: Chain):
    """
    Return the protocol SDK for the given web3 client
    """
def get_blocknative_tip(chain: Chain): ...
def read_config_file(config_file_name: str = 'config.json'): ...
def read_config_file_local(config_file_name: str = 'config.json'): ...
def read_config_file_gcs(config_file_name: str = 'config.json'):
    """
    Read the main configuration file from Google Cloud Storage. The path is provided via environment variables.
    """
def retry_get_block(block_number: int, web3: Web3): ...
