import pandas as pd
from src.data_monitoring.data.coingecko import coingecko_clip_window_days as coingecko_clip_window_days, coingecko_dex_get_pool_price as coingecko_dex_get_pool_price, coingecko_dex_get_pool_prices as coingecko_dex_get_pool_prices, coingecko_get_price as coingecko_get_price, coingecko_get_prices as coingecko_get_prices
from src.data_monitoring.data.get_cex_prices import format_pair_cex_binance as format_pair_cex_binance, get_cex_price as get_cex_price, get_cex_price_3way_pair as get_cex_price_3way_pair, get_cex_prices as get_cex_prices, get_cex_prices_3way_pair as get_cex_prices_3way_pair
from src.strategy.utils.base_model import ModelConfig as ModelConfig
from src.strategy.utils.pool_token import Pool as Pool, Token as Token
from src.strategy.utils.price_model import PriceModel as PriceModel
from src.strategy.utils.utils import DataFormat as DataFormat, DataSource as DataSource, ETHNativeChains as ETHNativeChains, convert_time_window as convert_time_window
from src.strategy.utils.volatility_model import VolatilityModel as VolatilityModel

COINGECKO_DEX_MISSING_DATA_BUFFER: float

def get_price_and_volatility(price_model: ModelConfig, volatility_model: ModelConfig, pool: Pool, granularity: str | None = '1h', price_window_multiplier: float | None = 1.0, volatility_window_multiplier: float | None = 1.0) -> tuple[pd.DataFrame, pd.DataFrame]: ...
def get_current_price_and_volatility(price_model: ModelConfig, volatility_model: ModelConfig, pool: Pool, granularity: str | None = '1h') -> tuple[int, int]: ...
def get_historical_prices(data_source: DataSource, pool: Pool, window: int, granularity: str | None = '1h', verbose: bool = False) -> pd.DataFrame:
    '''
    Retrieves historical price data for a specified pair of tokens from a DataSource.
    The granularity and time window for the price data are determined by the strategy\'s configuration.

    Args:
        data_source (DataSource): The data source to fetch the price data from. (e.g. DataSource.BINANCE)
        pool (Pool): The pool for which to fetch the price data, containing the Tokens information.
        window (int): The time window for the price data.
        granularity (str, optional): The granularity of the price data to fetch. Defaults to "1h".
        verbose (bool, optional): Whether to print verbose output. Defaults to False.

    Returns:
        DataFrame: DF of historical OHLCV for the token pair, adjusted for any necessary inversion.

    Raises:
        ValueError: If there is an issue fetching the prices, typically due to network or API errors,
                    or if the specified tokens are not properly recognized by the data source.

    Notes:
        - The function automatically adjusts for token pairs that are quoted in the opposite direction from the
        requested pair by inverting the price.

    '''
def get_current_price(data_source: DataSource, pool: Pool | None = None, base_symbol: str | None = None, quote_symbol: str | None = None, chain: str | None = None) -> float: ...
