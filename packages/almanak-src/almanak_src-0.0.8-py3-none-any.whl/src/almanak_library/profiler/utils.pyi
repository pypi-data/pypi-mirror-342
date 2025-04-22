from _typeshed import Incomplete
from src.almanak_library.profiler.time_block import ProfileType as ProfileType, TimeBlockHandler as TimeBlockHandler, TimeBlockTable as TimeBlockTable
from src.utils.config import Config as Config

IS_AGENT_DEPLOYMENT: Incomplete

def get_cached_metrics_handler(): ...
def time_block(name: str, type: ProfileType, strategy_id: str, strategy_state: Incomplete | None = None, strategy_substate: Incomplete | None = None, action_type: Incomplete | None = None, action_id: Incomplete | None = None): ...
