import uuid
from _typeshed import Incomplete
from pydantic import BaseModel
from src.almanak_library.enums import ExecutionStatus as ExecutionStatus, TransactionType as TransactionType
from src.utils.utils import deserialize_timestamp as deserialize_timestamp, serialize_timestamp as serialize_timestamp
from typing import Any

class Transaction(BaseModel):
    """
    Represents a blockchain transaction.

    Attributes:
        type (TransactionType): The type of the transaction.
        dict (Dict[str, Any]): The transaction details in dictionary format.
        action_id (uuid.UUID): The UUID of the associated action.
        id (uuid.UUID): A unique identifier for the transaction, generated at creation.
        tx_hash (Optional[str]): The transaction hash, which uniquely identifies the transaction
                                 on the blockchain. This is set after the transaction is signed and
                                 broadcasted.
        from_address (Optional[str]): The address from which the transaction originates.
        created_at (float): The timestamp when the transaction was created.

    Methods:
        get_type() -> TransactionType:
            Returns the type of the transaction.

        get_dict() -> Dict[str, Any]:
            Returns the transaction details as a dictionary.

        get_action_id() -> uuid.UUID:
            Returns the UUID of the associated action.

        get_id() -> str:
            Returns the unique identifier for the transaction. If the transaction hash (`tx_hash`) is available,
            it is returned as the ID. Otherwise, the UUID (`id`) generated at creation is returned.

        get_from_address() -> Optional[str]:
            Returns the address from which the transaction originates.

        get_created_at() -> float:
            Returns the timestamp when the transaction was created.

        __str__() -> str:
            Returns a string representation of the transaction, including its ID, type, action ID, creation time,
            and other relevant details.

        model_dump(*args, **kwargs) -> dict:
            Returns a dictionary representation of the transaction suitable for serialization. This includes converting
            types to their appropriate serialized forms and ensuring the correct ID (either `tx_hash` or `id`) is used.

        model_validate(cls, obj) -> 'Transaction':
            Validates and converts a dictionary representation of a transaction into a `Transaction` object, ensuring
            correct types and deserialization of fields.

        from_json(cls, json_str: str) -> 'Transaction':
            Creates a `Transaction` object from a JSON string representation.
    """
    type: TransactionType
    tx_dict: dict[str, Any]
    action_id: uuid.UUID
    id: uuid.UUID
    from_address: str | None
    tx_hash: str | None
    tx_status: ExecutionStatus | None
    created_at: float
    class Config:
        arbitrary_types_allowed: bool
        json_encoders: Incomplete
    def get_type(self) -> TransactionType: ...
    def get_dict(self) -> dict[str, Any]: ...
    def get_action_id(self) -> uuid.UUID: ...
    def get_id(self) -> uuid.UUID: ...
    def get_from_address(self) -> str | None: ...
    def get_created_at(self) -> float: ...
    def model_dump(self, *args, **kwargs): ...
    @classmethod
    def model_validate(cls, obj): ...
    @classmethod
    def from_json(cls, json_str: str): ...
