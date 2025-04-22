from _typeshed import Incomplete
from enum import Enum
from sqlmodel import SQLModel
from src.almanak_library.metrics.engine import get_metrics_engine as get_metrics_engine
from src.utils.config import Config as Config

STORAGE_DIR: Incomplete
LOCAL_DB_PATH: Incomplete
IS_AGENT_DEPLOYMENT: Incomplete
TIME_BLOCK_DB_CONNECTION_STRING: Incomplete

class ProfileType(Enum):
    BUILD_TRANSACTION = 'BUILD_TRANSACTION'
    EXECUTE_TRANSACTION = 'EXECUTE_TRANSACTION'
    SEND_TRANSACTION = 'SEND_TRANSACTION'
    SIGN_TRANSACTION = 'SIGN_TRANSACTION'
    WAIT_FOR_RECEIPT = 'WAIT_FOR_RECEIPT'
    PARSE_RECEIPT = 'PARSE_RECEIPT'
    STRATEGY = 'STRATEGY'
    POST_PROCESS = 'POST_PROCESS'
    TOTAL = 'TOTAL'

class TimeBlockTable(SQLModel, table=True):
    __tablename__: str
    id: int
    time: str
    name: str
    profile_type: str
    strategy_id: str
    strategy_state: str
    strategy_substate: str
    action_types: str
    action_id: str
    duration: float
    timing_metadata: dict
    __table_args__: Incomplete

class TimeBlockHandler:
    engine: Incomplete
    def __init__(self, db_connection_string: str = ...) -> None: ...
    def create_tables(self) -> None: ...
    def add(self, info: str) -> None: ...
    def get_time_block(self, strategy_id: str | None = None, profile_type: ProfileType | None = None, name_substr: str | None = None): ...
