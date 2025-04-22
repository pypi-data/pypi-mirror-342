import pydantic
from src.strategy.utils.utils import DataFormat as DataFormat, DataSource as DataSource
from typing import Any

class BaseModel:
    def __init__(self, data) -> None: ...

class ModelConfig(pydantic.BaseModel):
    method: str
    params: dict[str, Any]
    data_source: DataSource
    data_format: DataFormat
    def model_dump(self, **kwargs): ...
