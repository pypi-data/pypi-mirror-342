from _typeshed import Incomplete
from src.utils.config import Config as Config

IS_AGENT_DEPLOYMENT: Incomplete
storage_client: Incomplete

def get_keyfile(keyfile_name: str) -> str: ...
def get_secret(public_address: str, version_id: str = 'latest') -> str: ...
