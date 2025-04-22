import abc
from abc import ABC, abstractmethod
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from typing import Any

class CoSignerInterface(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self): ...
    @abstractmethod
    def sign_transactions(self, action_bundle: ActionBundle, cosigning_config: dict[str, Any]) -> ActionBundle: ...
