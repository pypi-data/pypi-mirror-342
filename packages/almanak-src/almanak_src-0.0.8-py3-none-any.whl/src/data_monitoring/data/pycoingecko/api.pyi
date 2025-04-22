from .utils import func_args_preprocessing as func_args_preprocessing
from _typeshed import Incomplete

CG_POOL_OHLCV_AGG_PERIODS: Incomplete

class CoinGeckoAPI:
    api_key: Incomplete
    api_base_url: Incomplete
    request_timeout: int
    session: Incomplete
    network_id_cache: Incomplete
    def __init__(self, api_key: str = '', retries: int = 5) -> None: ...
    def ping(self, **kwargs):
        """Check API server status"""
    def get_price(self, ids, vs_currencies, **kwargs):
        """Get the current price of any cryptocurrencies in any other supported currencies that you need"""
    def get_token_price(self, id, contract_addresses, vs_currencies, **kwargs):
        """Get the current price of any tokens on this coin (ETH only at this stage as per api docs) in any other supported currencies that you need"""
    def get_supported_vs_currencies(self, **kwargs):
        """Get list of supported_vs_currencies"""
    def get_coins(self, **kwargs):
        """List all coins with data (name, price, market, developer, community, etc)"""
    def get_coins_list(self, **kwargs):
        """List all supported coins id, name and symbol (no pagination required)"""
    def get_coins_markets(self, vs_currency, **kwargs):
        """List all supported coins price, market cap, volume, and market related data"""
    def get_coin_by_id(self, id, **kwargs):
        """Get current data (name, price, market, ... including exchange tickers) for a coin"""
    def get_coin_ticker_by_id(self, id, **kwargs):
        """Get coin tickers (paginated to 100 items)"""
    def get_coin_history_by_id(self, id, date, **kwargs):
        """Get historical data (name, price, market, stats) at a given date for a coin"""
    def get_coin_market_chart_by_id(self, id, vs_currency, days, **kwargs):
        """Get historical market data include price, market cap, and 24h volume (granularity auto)"""
    def get_coin_market_chart_range_by_id(self, id, vs_currency, from_timestamp, to_timestamp, **kwargs):
        """Get historical market data include price, market cap, and 24h volume within a range of timestamp (granularity auto)"""
    def get_coin_ohlc_by_id(self, id, vs_currency, days, **kwargs):
        """Get coin's OHLC"""
    def get_coin_info_from_contract_address_by_id(self, id, contract_address, **kwargs):
        """Get coin info from contract address"""
    def get_coin_market_chart_from_contract_address_by_id(self, id, contract_address, vs_currency, days, **kwargs):
        """Get historical market data include price, market cap, and 24h volume (granularity auto) from a contract address"""
    def get_coin_market_chart_range_from_contract_address_by_id(self, id, contract_address, vs_currency, from_timestamp, to_timestamp, **kwargs):
        """Get historical market data include price, market cap, and 24h volume within a range of timestamp (granularity auto) from a contract address"""
    def get_asset_platforms(self, **kwargs):
        """List all asset platforms (Blockchain networks)"""
    def get_coins_categories_list(self, **kwargs):
        """List all categories"""
    def get_coins_categories(self, **kwargs):
        """List all categories with market data"""
    def get_exchanges_list(self, **kwargs):
        """List all exchanges"""
    def get_exchanges_id_name_list(self, **kwargs):
        """List all supported markets id and name (no pagination required)"""
    def get_exchanges_by_id(self, id, **kwargs):
        """Get exchange volume in BTC and tickers"""
    def get_exchanges_tickers_by_id(self, id, **kwargs):
        """Get exchange tickers (paginated, 100 tickers per page)"""
    def get_exchanges_volume_chart_by_id(self, id, days, **kwargs):
        """Get volume chart data for a given exchange"""
    def get_indexes(self, **kwargs):
        """List all market indexes"""
    def get_indexes_by_market_id_and_index_id(self, market_id, id, **kwargs):
        """Get market index by market id and index id"""
    def get_indexes_list(self, **kwargs):
        """List market indexes id and name"""
    def get_derivatives(self, **kwargs):
        """List all derivative tickers"""
    def get_derivatives_exchanges(self, **kwargs):
        """List all derivative tickers"""
    def get_derivatives_exchanges_by_id(self, id, **kwargs):
        """List all derivative tickers"""
    def get_derivatives_exchanges_list(self, **kwargs):
        """List all derivative tickers"""
    def get_nfts_list(self, **kwargs):
        """List all supported NFT ids, paginated by 100 items per page, paginated to 100 items"""
    def get_nfts_by_id(self, id, **kwargs):
        """Get current data (name, price_floor, volume_24h ...) for an NFT collection. native_currency (string) is only a representative of the currency"""
    def get_nfts_by_asset_platform_id_and_contract_address(self, asset_platform_id, contract_address, **kwargs):
        """Get current data (name, price_floor, volume_24h ...) for an NFT collection. native_currency (string) is only a representative of the currency"""
    def get_exchange_rates(self, **kwargs):
        """Get BTC-to-Currency exchange rates"""
    def search(self, query, **kwargs):
        """Search for coins, categories and markets on CoinGecko"""
    def get_search_trending(self, **kwargs):
        """Get top 7 trending coin searches"""
    def get_global(self, **kwargs):
        """Get cryptocurrency global data"""
    def get_global_decentralized_finance_defi(self, **kwargs):
        """Get cryptocurrency global decentralized finance(defi) data"""
    def get_companies_public_treasury_by_coin_id(self, coin_id, **kwargs):
        """Get public companies data"""
    def get_id_from_contract(self, contract_address: str, chain_name: str = 'ethereum', **kwargs) -> str | None: ...
    def get_supported_networks(self, **kwargs):
        """
        Get supported networks with pagination
        https://docs.coingecko.com/reference/networks-list
        """
    def get_network_id(self, chain: str) -> str:
        """
        Get the network ID corresponding to the given chain.
        Uses a cached mapping to avoid fetching the entire list each time.
        """
    def get_pool_ohlcv_by_address(self, chain, pool_address, timeframe, agg_period, limit, before_timestamp: Incomplete | None = None, currency: str = 'token', **kwargs):
        """
        Get pool's OHLCV data
        https://docs.coingecko.com/reference/pool-ohlcv-contract-address
        """
    def get_token_price_by_address(self, chain, addresses, **kwargs):
        """
        Get token price by address
        https://docs.coingecko.com/reference/token_price

        When using this endpoint, GeckoTerminal's routing decides the best pool for token price.
        The price source may change based on liquidity and pool activity.
        """
    def get_pool_data_by_address(self, chain, pool_address, **kwargs):
        """
        Get pool data by address
        https://docs.coingecko.com/reference/pool-address
        """
    def get_pool_tokens_by_address(self, chain, pool_address, **kwargs):
        """
        Get pool tokens by address
        https://docs.coingecko.com/reference/pool-token-info-contract-address
        """
