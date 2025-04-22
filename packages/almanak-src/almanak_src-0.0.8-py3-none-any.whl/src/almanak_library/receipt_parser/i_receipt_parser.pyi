import abc
from abc import ABC, abstractmethod
from web3 import Web3 as Web3

class IReceiptParser(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, web3: Web3): ...
