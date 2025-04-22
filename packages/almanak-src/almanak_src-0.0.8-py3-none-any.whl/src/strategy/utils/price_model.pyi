from _typeshed import Incomplete
from src.strategy.utils.base_model import BaseModel as BaseModel

class PriceModel(BaseModel):
    price_data: Incomplete
    def __init__(self, data) -> None:
        """
        Initialize the PriceModel with data.

        :param data: DataFrame with OHLCV columns or Series/array-like of close prices.
        """
    def raw(self):
        """
        Return the raw price data without any transformation.

        :return: Series, the original price data.
        """
    def sma(self, window):
        """
        Calculate the Simple Moving Average (SMA).

        :param window: Integer, the window size for SMA.
        :return: Series, the SMA values.
        """
    def ema(self, window):
        """
        Calculate the Exponential Moving Average (EMA).

        :param window: Integer, the window size for EMA.
        :return: Series, the EMA values.
        """
    def hma(self, window):
        """
        Calculate the Hull Moving Average (HMA).

        :param window: Integer, the window size for HMA.
        :return: Series, the HMA values.
        """
    def wma(self, window):
        """
        Calculate the Weighted Moving Average (WMA).

        :param window: Integer, the window size for WMA.
        :return: Series, the WMA values.
        """
    def tma(self, window):
        """
        Calculate the Triangular Moving Average (TMA).

        :param window: Integer, the window size for TMA.
        :return: Series, the TMA values.
        """
    def kama(self, window):
        """
        Calculate the Kaufman's Adaptive Moving Average (KAMA).

        :param window: Integer, the window size for KAMA.
        :return: Series, the KAMA values.
        """
    def model(self, model_type, window):
        """
        Select the price model to use.

        :param model_type: String, the type of model ('raw', 'sma', 'ema', 'hma', 'wma', 'tma', 'kama').
        :param window: Integer, the window size for the model. Not used for 'raw' model type.
        :return: Series, the calculated model values.
        """
    @classmethod
    def get_data_window(cls, model_type, window):
        """
        Calculate the required minimum data length for each model type.

        Note: These are minimum requirements. For better initialization,
        especially for models like EMA, consider using 2x or 3x the window size.

        :param model_type: String, the type of model ('raw', 'sma', 'ema', 'hma', 'wma', 'tma', 'kama').
        :param window: Integer, the window size for the model. Not used for 'raw' model type.
        :return: Integer, the required data length for the specified model.
        """
