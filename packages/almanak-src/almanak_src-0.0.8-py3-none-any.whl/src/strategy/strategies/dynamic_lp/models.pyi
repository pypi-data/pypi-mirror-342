from _typeshed import Incomplete
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, confloat as confloat, conint as conint
from src.almanak_library.enums import Chain as Chain, Network as Network, Protocol as Protocol
from src.strategy.models import InternalFlowStatus as InternalFlowStatus, PersistentStateBase as PersistentStateBase, StrategyConfigBase as StrategyConfigBase
from src.strategy.utils.utils import DataFormat as DataFormat, DataSource as DataSource
from typing import Any
from uuid import UUID

class State(Enum):
    """Enum representing the state of the strategy."""
    INITIALIZATION = 'INITIALIZATION'
    CHECK_FOR_REBALANCE = 'CHECK_FOR_REBALANCE'
    CLOSE_POSITION = 'CLOSE_POSITION'
    SWAP_ASSETS = 'SWAP_ASSETS'
    OPEN_POSITION = 'OPEN_POSITION'
    COMPLETED = 'COMPLETED'
    TEARDOWN = 'TEARDOWN'
    TERMINATED = 'TERMINATED'

class SubState(Enum):
    """Enum representing the substates of some of the strategy states. A state machine within a state machine."""
    NO_SUBSTATE = 'NO_SUBSTATE'
    INITIALIZATION_SWAP0 = 'INITIALIZATION_SWAP0'
    INITIALIZATION_SWAP1 = 'INITIALIZATION_SWAP1'
    INITIALIZATION_OPEN = 'INITIALIZATION_OPEN'
    TEARDOWN_CLOSE = 'TEARDOWN_CLOSE'
    TEARDOWN_SWAP0 = 'TEARDOWN_SWAP0'
    TEARDOWN_SWAP1 = 'TEARDOWN_SWAP1'
    TEARDOWN_UNWRAP = 'TEARDOWN_UNWRAP'

class PersistentState(PersistentStateBase):
    current_state: State
    current_substate: SubState
    current_flowstatus: InternalFlowStatus
    current_actions: list[UUID]
    sadflow_counter: int
    sadflow_actions: list[UUID]
    not_included_counter: int
    position_id: int
    last_close_amounts_total: tuple[int, int]
    last_close_amounts_fees: tuple[int, int]
    last_close_amounts_liquidity: tuple[int, int]
    last_open_amounts: tuple[int, int]
    last_open_bounds: tuple[int, int]
    last_open_unallocated_amounts: tuple[int, int]
    last_open_model_price: float
    last_swap_amounts: tuple[int, int]
    initialize_token_amounts: tuple[int, int]
    teardown_close_amounts_total: tuple[int, int]
    teardown_swap_amounts: tuple[int, int]
    teardown_unwrap_target_amount: int
    teardown_unwrap_amount: int
    last_rebalance_time: datetime
    initialized_time: datetime
    class Config:
        arbitrary_types_allowed: bool
        json_encoders: Incomplete
    def model_dump(self, **kwargs): ...

class InitializationConfig(BaseModel):
    initial_position_value_USD: None
    initial_funding_token: str
    initial_token0_pool: str
    initial_token1_pool: str

class ModelConfig(BaseModel):
    method: str
    params: dict[str, Any]
    data_source: DataSource
    data_format: DataFormat
    def model_dump(self, **kwargs): ...

class StrategyConfig(StrategyConfigBase):
    id: str
    network: Network
    chain: Chain
    protocol: Protocol
    wallet_address: str
    max_sadflow_retries: int
    max_not_included_retries: int
    initiate_teardown: bool
    pause_strategy: bool
    granularity: str
    time_window: int
    volatility_factor: int
    pool_address: str
    rebalance_price_bounds: None
    initialization: InitializationConfig
    rebalance_frequency: int | None
    run_duration: int | None
    data_source: DataSource | None
    price_model: ModelConfig | None
    volatility_model: ModelConfig | None
    def validate_ethereum_address(cls, value): ...
    def model_dump(self, *args, **kwargs): ...
