from _typeshed import Incomplete
from typing import Any

class GraphQLClient:
    """
    A client for interacting with a GraphQL API.
    """
    logger: Incomplete
    url: Incomplete
    headers: Incomplete
    def __init__(self, url: str, api_key: str, logger: Incomplete | None = None) -> None: ...
    def execute(self, query: dict, variables: dict[str, str] = None) -> Any:
        """
        Execute a GraphQL query.
        """

class HasuraClient:
    """
    A client for interacting with the Multiverse Platform API.
    """
    graphql_client: Incomplete
    user_id: Incomplete
    team_id: Incomplete
    organisation_id: Incomplete
    api_key: Incomplete
    logger: Incomplete
    def __init__(self, api_url, platform_jwt, is_jwt: bool = False, logger: Incomplete | None = None) -> None: ...
    def get_user_id(self):
        """
        Get the user id from api_key object the graphql client
        """
    def get_user_team(self):
        """
        Get the user id, team id and organisation id from the graphql client
        """
    def print_config(self) -> None:
        """
        Print the user id, team id and organisation id
        """
    def get_block_height_by_time(self, timestamp):
        """
        Get the block height by time
        """
    def get_prices_mcV3(self, assets, config, drift, end_block, granularity, start_block, steps, trajectories, volatilityMode): ...
    def wait_for_prices(self, request_id: str):
        """
        Waits for the completion of the price data simulation and returns the results.

        Parameters:
        - request_id: The ID of the simulation request.
        """
