import abc
import uuid
from _typeshed import Incomplete
from abc import ABC
from pydantic import BaseModel
from src.almanak_library.enums import ActionType as ActionType, SwapSide as SwapSide
from typing import Any

class Receipt(BaseModel, ABC, metaclass=abc.ABCMeta):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    class Config:
        arbitrary_types_allowed: bool
        json_encoders: Incomplete
    def model_dump(self, exclude: set[str] = ...) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Receipt: ...

class WrapReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    amount: int

class UnwrapReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    amount: int

class ApproveReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int

class OpenPositionReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    token0_symbol: str
    token1_symbol: str
    amount0: int
    amount1: int
    position_id: int
    bound_tick_lower: int
    bound_tick_upper: int
    bound_price_lower: float
    bound_price_upper: float
    pool_tick: int | None
    pool_spot_rate: float | None

class SwapReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    side: SwapSide
    tokenIn_symbol: str
    tokenOut_symbol: str
    amountIn: int
    amountOut: int
    def model_dump(self, *args, **kwargs): ...

class ClosePositionReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    position_id: int
    token0_symbol: str
    token1_symbol: str
    amount0: int
    amount1: int
    liquidity0: int
    liquidity1: int
    fees0: int
    fees1: int
    pool_tick: int | None
    pool_spot_rate: float | None
