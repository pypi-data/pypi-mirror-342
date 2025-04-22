import uuid
from _typeshed import Incomplete
from pydantic import BaseModel
from src.almanak_library.enums import ActionType as ActionType, Protocol as Protocol
from src.almanak_library.models.params import Params as Params
from src.almanak_library.models.receipt import Receipt as Receipt
from src.almanak_library.models.transaction import Transaction as Transaction

def default_list(): ...

class Action(BaseModel):
    type: ActionType
    params: Params
    protocol: Protocol
    id: uuid.UUID
    execution_details: Receipt | None
    transactions: list[Transaction]
    transaction_hashes: list[str]
    bundle_id: uuid.UUID | None
    class Config:
        arbitrary_types_allowed: bool
        json_encoders: Incomplete
    def get_id(self) -> uuid.UUID: ...
    def get_type(self) -> ActionType: ...
    def get_params(self) -> Params: ...
    def get_protocol(self) -> Protocol: ...
    def get_execution_details(self) -> Receipt | None: ...
    def model_dump(self, *args, **kwargs): ...
    @classmethod
    def model_validate(cls, obj): ...
    @classmethod
    def from_json(cls, json_str: str): ...
