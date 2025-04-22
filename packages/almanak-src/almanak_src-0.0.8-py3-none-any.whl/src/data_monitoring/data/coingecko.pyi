import pandas as pd
from _typeshed import Incomplete
from src.data_monitoring.data.pycoingecko.api import CG_POOL_OHLCV_AGG_PERIODS as CG_POOL_OHLCV_AGG_PERIODS, CoinGeckoAPI as CoinGeckoAPI
from src.strategy.utils.pool_token import Pool as Pool, Token as Token
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger

logger: Incomplete
COINGECKO_API_KEY: Incomplete
COINGECKO_DEX_OHLCV_LIMIT: int
cg: Incomplete
token_id_from_address_cache: Incomplete

def coingecko_get_token_id_from_address(contract_address: str, chain_name: str) -> str: ...
def coingecko_check_pair(token0: Token, token1: Token) -> bool:
    """
    # TODO: Use the vs_currency, but for now it's all 3-way pairs using USD.
    """
def coingecko_get_price(token0: Token, token1: Token) -> float:
    '''
    Fetches the "3-way" price of token0 against token1.

    Returns the price of token0 in terms of token1
    '''
def coingecko_get_supported_vs_currencies() -> list: ...
def coingecko_get_coins_list() -> pd.DataFrame: ...
def coingecko_get_prices(token0: Token, token1: Token, days: int, interval: str = '1h') -> dict:
    """
    Fetches OHLC data for token0 and token1 over a period of time and computes the 3-way price.

    :param token0: The first token symbol (e.g., 'BTC')
    :param token1: The second token symbol (e.g., 'ETH') can be None for a single token vs USD
    :param days: The number of days of historical data to fetch
    :param interval: The granularity of the data ('1h', '1d', 'hourly', 'daily')
    :param price_type: The price type to return ('open', 'close', 'high', 'low', 'ohlc')
    :param use_symbols: Whether to use symbols to fetch the token IDs
    :return: A dictionary containing the time series of adjusted prices
    """
def coingecko_clip_window_days(window_days: int, granularity: str) -> int:
    """
    Adjusts window_days to the next available quantity possible based on granularity.
    Coingecko API supports only certain day intervals for hourly and daily data.
    https://docs.coingecko.com/reference/coins-id-ohlc

    :param window_days: Number of days to clip.
    :param granularity: The granularity of the data ('1h' for hourly, '1d' for daily).
    :return: The adjusted window_days.
    """
def coingecko_dex_get_pool_prices(pool: Pool, granularity: str, start_date: Incomplete | None = None, end_date: Incomplete | None = None, window: Incomplete | None = None, limit: Incomplete | None = None, currency: str = 'token', verbose: bool = False): ...
def coingecko_dex_get_pool_data(pool: Pool, verbose: bool = False):
    """
    Fetches pool data from CoinGecko DEX API.

    Response example:
    {'data': {'id': 'arbitrum_0x53c6ca2597711ca7a73b6921faf4031eedf71339',
    'type': 'pool',
    'attributes': {'base_token_price_usd': '60000.5164933544',
    'base_token_price_native_currency': '25.8246677226086',
    'quote_token_price_usd': '1.000273906851',
    'quote_token_price_native_currency': '0.000430525315209306',
    'base_token_price_quote_token': '59984.09',
    'quote_token_price_base_token': '0.00001667',
    'address': '0x53c6ca2597711ca7a73b6921faf4031eedf71339',
    'name': 'WBTC / USDT 0.3%',
    'pool_created_at': '2022-02-08T00:28:18Z',
    'fdv_usd': '617173296',
    'market_cap_usd': '617470746.878951',
    'price_change_percentage': {'m5': '0',
        'h1': '-0.2',
        'h6': '0.01',
        'h24': '3.76'},
    'transactions': {'m5': {'buys': 0, 'sells': 1, 'buyers': 0, 'sellers': 1},
        'm15': {'buys': 0, 'sells': 1, 'buyers': 0, 'sellers': 1},
        'm30': {'buys': 0, 'sells': 1, 'buyers': 0, 'sellers': 1},
        'h1': {'buys': 1, 'sells': 1, 'buyers': 1, 'sellers': 1},
        'h24': {'buys': 574, 'sells': 277, 'buyers': 164, 'sellers': 95}},
    'volume_usd': {'m5': '0.974947971803437',
        'h1': '4946.8101008762',
        'h6': '134609.00822283',
        'h24': '831714.447482519'},
    'reserve_in_usd': '2164769.0213'},
    'relationships': {'base_token': {'data': {'id': 'arbitrum_0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f',
        'type': 'token'}},
    'quote_token': {'data': {'id': 'arbitrum_0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9',
        'type': 'token'}},
    'dex': {'data': {'id': 'uniswap_v3_arbitrum', 'type': 'dex'}}}}}

    -----
    IMPORTANT: The order of the pool could be inverted!
               The base token could be token1 and the quote token could be token0.
    """
def coingecko_dex_get_pool_price(pool: Pool, verbose: bool = False):
    """
    Args:
        chain (str): Chain
        pool_address (str): Pool Address
        verbose (bool, optional): Defaults to False.

    Returns:
        pool_price (T0/T1), token0_price_USD, token1_price_USD, token0_price_native_currency, token1_price_native_currency
    """
