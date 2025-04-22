from _typeshed import Incomplete
from sqlalchemy.future.engine import Engine as Engine
from src.utils.config import Config as Config

STORAGE_DIR: Incomplete
LOCAL_DB_PATH: Incomplete
READ_ONLY_MODE: Incomplete
IS_AGENT_DEPLOYMENT: Incomplete
METRICS_DB_CONNECTION_STRING: Incomplete

def get_metrics_engine(db_connection_string: str = ...) -> Engine: ...
