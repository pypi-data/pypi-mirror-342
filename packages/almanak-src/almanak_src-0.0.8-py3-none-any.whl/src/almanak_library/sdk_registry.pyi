from _typeshed import Incomplete
from src.almanak_library.enums import Chain as Chain, Network as Network, Protocol as Protocol
from src.almanak_library.models.sdk import ISDK as ISDK

class SDKRegistry:
    def __init__(self) -> None: ...
    def register_sdk(self, protocol: Protocol, network: Network, chain: Chain, sdk_class: type[ISDK]): ...
    def get_sdk_class(self, protocol: Protocol, network: Network, chain: Chain) -> type[ISDK]: ...

sdk_registry: Incomplete
