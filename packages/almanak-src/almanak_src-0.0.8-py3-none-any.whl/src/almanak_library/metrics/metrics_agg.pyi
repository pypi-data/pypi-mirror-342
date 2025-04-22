from _typeshed import Incomplete
from enum import Enum
from sqlmodel import SQLModel
from src.almanak_library.metrics.engine import get_metrics_engine as get_metrics_engine
from src.utils.config import Config as Config

STORAGE_DIR: Incomplete
LOCAL_DB_PATH: Incomplete
IS_AGENT_DEPLOYMENT: Incomplete
METRICS_DB_CONNECTION_STRING: Incomplete

def default_agent_id(): ...
def default_user_id(): ...

class MetricAggType(Enum):
    INITIALIZATION = 'INITIALIZATION'
    TEARDOWN = 'TEARDOWN'
    STRATEGY_BALANCE = 'STRATEGY_BALANCE'
    WALLET_BALANCE = 'WALLET_BALANCE'
    SNAPSHOT = 'SNAPSHOT'
    REBALANCE_TRIGGER = 'REBALANCE_TRIGGER'

class MetricsAggTable(SQLModel, table=True):
    __tablename__: str
    id: int
    time: str
    block_number: int | None
    metric_type: str
    strategy_id: str
    action_id: str
    bundle_id: str
    wallet_address: str
    details: dict
    agent_id: str | None
    user_id: str | None
    __table_args__: Incomplete

class MetricsAggHandler:
    engine: Incomplete
    def __init__(self, db_connection_string) -> None: ...
    def create_tables(self) -> None: ...
    def add_metric(self, metric: MetricsAggTable) -> None: ...
    def get_metrics_agg(self, user_id: str = ..., agent_id: str = ..., strategy_id: str | None = None, metric_type: MetricAggType | str | None = None, wallet_address: str | None = None): ...
