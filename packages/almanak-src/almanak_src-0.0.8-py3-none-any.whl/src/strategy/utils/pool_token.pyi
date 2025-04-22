from _typeshed import Incomplete
from src.almanak_library.enums import Chain as Chain, Network as Network, Protocol as Protocol

class Token:
    contract: Incomplete
    address: Incomplete
    decimals: Incomplete
    symbol: Incomplete
    chain: Incomplete
    def __init__(self, contract, address: str, decimals: int, symbol: str, chain: str) -> None: ...
    def to_dict(self): ...
    def to_json(self): ...

class Pool:
    contract: Incomplete
    address: Incomplete
    token0: Incomplete
    token1: Incomplete
    fee: Incomplete
    chain: Incomplete
    protocol: Incomplete
    def __init__(self, contract, address: str, token0: Token, token1: Token, fee: int, chain: str, protocol: str) -> None: ...
    def get_reserves(self, pool_address): ...
    def to_dict(self): ...
    def to_json(self): ...

class PoolTokenRegistry:
    protocol: Incomplete
    chain: Incomplete
    network: Incomplete
    web3: Incomplete
    pools: Incomplete
    tokens: Incomplete
    pool_abi: Incomplete
    token_abi: Incomplete
    def __init__(self, protocol: Protocol, chain: Chain, network: Network, web3, pool_abi, token_abi) -> None: ...
    def get_pool(self, pool_address): ...
    def get_token(self, token_address): ...

class PoolTokenService:
    def __init__(self) -> None: ...
    def get_registry(self, protocol: Protocol, chain: Chain, network: Network, web3, pool_abi, token_abi) -> PoolTokenRegistry: ...

pooltoken_service: Incomplete
