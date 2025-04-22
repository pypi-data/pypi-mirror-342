from _typeshed import Incomplete
from google.api_core.exceptions import GoogleAPICallError as GoogleAPICallError, NotFound as NotFound
from retry import retry as retry
from src.almanak_library.constants import MainStatus as MainStatus
from src.almanak_library.custom_exceptions import SimulationError as SimulationError
from src.almanak_library.init_sdk import initialize_sdks as initialize_sdks
from src.almanak_library.profiler.time_block import ProfileType as ProfileType
from src.almanak_library.profiler.utils import time_block as time_block
from src.executer.execution_manager import ExecutionManager as ExecutionManager
from src.post_processing.post_process_manager import PostProcessManager as PostProcessManager
from src.signer.account_manager import AccountManager as AccountManager
from src.strategy.strategy_factory import create_strategy_from_config as create_strategy_from_config, get_strategy_ids_from_config as get_strategy_ids_from_config
from src.strategy.strategy_id_iterator import StrategyIDIterator as StrategyIDIterator
from src.transaction_builder.builder_manager import TransactionManager as TransactionManager
from src.utils.agent_machine_status import AgentMachineState as AgentMachineState, upload_agent_machine_file as upload_agent_machine_file
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger, get_non_alert_logger as get_non_alert_logger, setup_logging as setup_logging
from src.utils.utils import read_config_file as read_config_file

logger: Incomplete
IS_AGENT_DEPLOYMENT: Incomplete
DEBUG: Incomplete
storage_client: Incomplete
cloud_logging_service_name: Incomplete
cloud_logger: Incomplete
STORAGE_DIR: Incomplete
MAX_ALLOWED_EXCEPTIONS_IN_WINDOW: int
ROLLING_WINDOW_MINUTES: int
rolling_time_window: Incomplete
exception_tracker: Incomplete
MAINLOOP_DELAY_SECONDS: Incomplete
SHUTDOWN: Incomplete
READ_ONLY_MODE: Incomplete
CONFIG_FILE_NAME: str

def single_main_iteration(config: dict, strategy_id: str):
    """
    Runs a single iteration of the main loop for a given strategy.
    If the strategy raises/crashes, the main will loop thru other strategies and come back to this one later.
    """
def main(strategy_id_iterator: StrategyIDIterator, strategy_ids: list = None):
    """
    Continuously run the main iteration of the enterprise service.
    The retry function has exponential backoff and jitter to prevent
    overloading the system with retries.

    NOTE: This is a simple retry mechanism. It is not a robust solution
    for handling errors. It is only used to prevent the service from
    crashing due to transient errors.

    NOTE: This could cause a cascading alerts if the error is not transient.
    """
def exponential_backoff_with_jitter(retry_count, base_delay: int = 1, max_delay: int = 60): ...
def super_main() -> None:
    """
    If any errors are raised, just retry the main function
    """
