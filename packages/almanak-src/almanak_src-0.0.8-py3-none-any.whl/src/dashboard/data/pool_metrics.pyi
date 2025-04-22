from _typeshed import Incomplete

class PoolMetrics:
    prices: Incomplete
    log_returns: Incomplete
    price_changes: Incomplete
    percent_changes: Incomplete
    def __init__(self, prices) -> None:
        """
        Initialize the PoolMetrics class with a series of prices.
        
        :param prices: pandas Series of price data
        """
    def calc_mean_drift(self):
        """
        Calculate mean drift based on log returns and price changes.
        
        :return: tuple (return_drift, price_drift, price_drift_pct)
        """
    def calc_mean_volatility(self):
        """
        Calculate mean volatility based on log returns and price changes.
        
        :return: tuple (return_volatility, price_volatility, price_volatility_pct)
        """
    def calc_all_mean_metrics(self):
        """
        Calculate all mean metrics: mean drift and mean volatility.
        
        :return: tuple (return_drift, price_drift, price_drift_pct, return_volatility, price_volatility, price_volatility_pct)
        """
    @staticmethod
    def random_bm(mu, sigma):
        """
        Generate a random number using Box-Muller transform.
        
        :param mu: Mean
        :param sigma: Standard deviation
        :return: Random number
        """
    @staticmethod
    def calc_imp_loss(lower_limit, upper_limit, px, alpha):
        """
        Calculate impermanent loss.
        
        :param lower_limit: Lower price limit
        :param upper_limit: Upper price limit
        :param px: Current price
        :param alpha: Alpha parameter
        :return: Impermanent loss
        """
    def calc_exp_imp_loss(self, range_perc, mu, sigma, alpha):
        """
        Calculate expected impermanent loss.
        
        :param range_perc: Range percentage
        :param mu: Mean
        :param sigma: Standard deviation
        :param alpha: Alpha parameter
        :return: Expected impermanent loss
        """
    def calc_iv(self, range_perc, mu, alpha):
        """
        Calculate implied volatility.
        
        :param range_perc: Range percentage
        :param mu: Mean
        :param alpha: Alpha parameter
        :return: Implied volatility
        """
