import abc
from abc import ABC, abstractmethod
from src.almanak_library.enums import Chain as Chain, Network as Network

class ISDK(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, network: Network, chain: Chain): ...
