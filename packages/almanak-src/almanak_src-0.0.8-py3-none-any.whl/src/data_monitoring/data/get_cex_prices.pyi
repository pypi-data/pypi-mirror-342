from _typeshed import Incomplete
from src.utils.logger import get_logger as get_logger

logger: Incomplete

def format_pair_cex_binance(token0, token1):
    """
    Formats the given tokens for Binance's asset pair format and checks if the pair is supported.
    Removes 'W' prefix from wrapped tokens, tries the pair, and if not supported, tries the inverse.

    :param token0: The first token of the pair (e.g., 'WBTC')
    :param token1: The second token of the pair (e.g., 'WETH')
    :return: A tuple containing the formatted pair string and a boolean indicating if the pair was inverted.
             return None, None if the pair is not supported.

    ### DANGER ###
    TODO: For now we remove W is first letter, but this is not the correct way to handle wrapped tokens.
    We should check if the token is wrapped and then remove the W prefix.
    i.e. we currently don't support real tokens that start with W.
    ### DANGER ###
    """
def check_pair_cex_binance(pair):
    """
    Checks if a given asset pair is supported on Binance by attempting to fetch its price data.

    :param pair: The asset pair string (e.g., 'BTCUSDT')
    :return: True if the pair is supported, False otherwise.
    """
def get_ohlcv_data(pair, interval, start_time, end_time):
    """
    Fetches OHLCV data for a list of asset pairs from the Binance API.

    :param pair: Asset pair string (e.g., 'BTCUSDT' or 'ETHUSDT')
    :param interval: Interval for klines (e.g., '1h', '1d')
    :param start_time: Start time for data in 'YYYY-mm-dd HH:MM:SS' format
    :param end_time: End time for data in 'YYYY-mm-dd HH:MM:SS' format
    :return: Dictionary with asset pairs as keys and OHLC data as values

    Using the API directly instead of any SDKs.
    The usage is quite simple and small, so it's easier to handle manually directly via URL requests.
    """
def invert_ohlcv(df):
    """
    Inverts OHLCV data by taking the reciprocal of the prices.

    :param df: DataFrame containing OHLCV data
    :return: DataFrame with inverted OHLCV data
    """
def get_cex_prices(asset_pair, interval, start_time, end_time, invert: bool = False): ...
def get_cex_prices_3way_pair(token0, token1, intermediary, interval, start_time, end_time): ...
def get_cex_price(asset_pair): ...
def get_cex_price_3way_pair(token0, token1, intermediary): ...
