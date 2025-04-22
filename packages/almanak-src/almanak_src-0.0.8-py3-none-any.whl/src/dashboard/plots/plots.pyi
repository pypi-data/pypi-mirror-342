from _typeshed import Incomplete
from src.strategy.utils.base_model import ModelConfig as ModelConfig
from src.strategy.utils.price_model import PriceModel as PriceModel
from src.strategy.utils.price_volatility import get_historical_prices as get_historical_prices
from src.strategy.utils.utils import DataFormat as DataFormat, convert_time_window as convert_time_window

PLOT_TITLE_FONT_SIZE: int

def plot_liquidity_distribution(all_processed_ticks, pool, position_info: Incomplete | None = None, simple: bool = False): ...
def plot_positions_over_time(positions, data_source, pool, data_format: str = 'close', granularity: str = '1h', start_time: Incomplete | None = None, end_time: Incomplete | None = None, price_model: ModelConfig = None, volatility_model: ModelConfig = None, hedge_trades: Incomplete | None = None, price_bounds_config: Incomplete | None = None): ...
