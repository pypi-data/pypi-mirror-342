from src.strategy.utils.base_model import BaseModel as BaseModel

class VolatilityModel(BaseModel):
    """
    A class for calculating various volatility models on financial data.

    This class inherits from BaseModel and provides methods to calculate
    different volatility indicators such as ATR, Standard Deviation,
    Bollinger Bands, RVI, and Normalized Standard Deviation.

    Attributes:
        data (pd.DataFrame or pd.Series): The input financial data.
        data_format (str): The type of input data ('ohlcv' or 'close').
    """
    def __init__(self, data) -> None:
        """
        Initialize the VolatilityModel with the given data.

        Args:
            data (pd.DataFrame or pd.Series): The input financial data.
        """
    def atr(self, window, scalar: int = 1):
        """
        Calculate the Average True Range (ATR) and its bounds.

        Args:
            window (int): The rolling window for ATR calculation.
            scalar (float, optional): Multiplier for the upper and lower bounds. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame containing ATR, Upper Bound, and Lower Bound.
        """
    def std(self, window, scalar: int = 1):
        """
        Calculate the Standard Deviation (STD) and its bounds.

        Args:
            window (int): The rolling window for STD calculation.
            scalar (float, optional): Multiplier for the upper and lower bounds. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame containing STD, Upper Bound, and Lower Bound.
        """
    def bollinger_bands(self, window, scalar: int = 2):
        """
        Calculate the Bollinger Bands (BB) and Bollinger Bandwidth (BBW).

        Args:
            window (int): The rolling window for BB calculation.
            scalar (float, optional): Number of standard deviations for the bands. Defaults to 2.

        Returns:
            pd.DataFrame: A DataFrame containing BBW, Upper Bound, and Lower Bound.
        """
    def rvi(self, window, scalar: int = 1):
        """
        Calculate the Relative Volatility Index (RVI) and its bounds.

        Args:
            window (int): The rolling window for RVI calculation.
            scalar (float, optional): Multiplier for the upper and lower bounds. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame containing RVI, Upper Bound, and Lower Bound.
        """
    def normalized_std(self, window, scalar: int = 1):
        """
        Calculate the Normalized Standard Deviation and its bounds.

        The Normalized STD is calculated as mean(std) / max(std) over the given window.

        Args:
            window (int): The rolling window for the calculation.
            scalar (float, optional): Multiplier for the upper and lower bounds. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame containing Normalized STD, Upper Bound, and Lower Bound.
        """
    def model(self, model_type, window, scalar: int = 1):
        """
        Select and calculate the specified volatility model.

        Args:
            model_type (str): The type of model to use.
                              Options: 'std', 'atr', 'bb', 'rvi', or 'normalized_std'.
            window (int): The rolling window for the model calculation.
            scalar (float, optional): Multiplier for bounds or bands. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame containing the calculated model values and bounds.

        Raises:
            ValueError: If an unrecognized model type is provided.
        """
    @classmethod
    def get_data_window(cls, model_type, window):
        """
        Calculate the required minimum data length for each model type.

        :param model_type: String, the type of model (e.g. 'std', 'atr', 'bb')
        :param window: Integer, the window size for the model.
        :return: Integer, the required data length for the specified model.
        """
