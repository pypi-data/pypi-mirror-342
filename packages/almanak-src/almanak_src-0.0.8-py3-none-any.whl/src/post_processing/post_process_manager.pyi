from _typeshed import Incomplete
from pathlib import Path as Path
from src.almanak_library.constants import MessageStatus as MessageStatus
from src.almanak_library.metrics.metrics_logger import MetricsLogger as MetricsLogger
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.post_processing.internal_messaging import InternalMessaging as InternalMessaging
from src.utils.config import Config as Config
from src.utils.utils import upload_transactions_for_agent as upload_transactions_for_agent

IS_AGENT_DEPLOYMENT: Incomplete

class PostProcessManager:
    internal_messaging: Incomplete
    metrics_logger: Incomplete
    def __init__(self) -> None: ...
    def process_bundle(self, action_bundle: ActionBundle) -> MessageStatus: ...
    def send_internal_message(self, action_bundle: ActionBundle) -> MessageStatus: ...
    def store_bundle_metrics(self, action_bundle: ActionBundle): ...
    def store_agent_transaction_data(self, action_bundle: ActionBundle): ...
