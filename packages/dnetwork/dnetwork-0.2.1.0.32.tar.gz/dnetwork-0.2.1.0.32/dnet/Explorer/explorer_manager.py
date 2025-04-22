import json
import logging

from dnet.Api.api_manager import ApiManager
from dnet.Explorer.graphql_queries import (
    GET_BLOCKCHAIN_EXPLORER,
    GET_BLOCKCHAIN_EXPLORER_BY_SEARCH,
    GET_NEW_BLOCK_SUBSCRIPTION,
)
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport

logging.getLogger("gql.transport.websockets").setLevel(logging.WARNING)

class ExplorerManager:
    def __init__(self, api_manager: ApiManager, subscription_url: str):
        """
        Initialize the ExplorerManager with an instance of ApiManager for HTTP queries
        and a subscription URL for real-time updates via WebSocket.
        
        :param api_manager: Instance of ApiManager (HTTP transport) for executing GraphQL queries.
        :param subscription_url: WebSocket URL for GraphQL subscriptions (e.g., "ws://203.0.113.2:8000/api/graphql").
        """
        self.api_manager = api_manager
        self.subscription_url = subscription_url

    def get_blockchain_explorer(self, height):
        """
        Retrieve blockchain explorer details by block height using HTTP transport.
        
        :param height: The block height to query.
        :return: The response from the GraphQL query.
        """
        variables = {"height": height}
        response = self.api_manager._execute_graphql(GET_BLOCKCHAIN_EXPLORER, variables)
        return response

    def get_blockchain_explorer_by_search(self, address=None, block=None, tx_hash=None, token=None):
        """
        Searches the blockchain explorer based on various parameters.
        The search input should be a dictionary containing one of the following keys:
          - address
          - block
          - tx_hash
          - token
        
        :param address: (Optional) The blockchain address to search.
        :param block: (Optional) The block number to search.
        :param tx_hash: (Optional) The transaction hash to search.
        :param token: (Optional) The token to search.
        :return: The response from the GraphQL search query.
        """
        variables = {
            "input": {
                "address": address,
                "block": block,
                "txHash": tx_hash,
                "token": token

            }
        }
        response = self.api_manager._execute_graphql(GET_BLOCKCHAIN_EXPLORER_BY_SEARCH, variables)
        return response

    async def subscribe_new_block(self):
        """
        Asynchronously subscribes to new block events using a WebSocket transport.
        
        :yield: Each new block event as it arrives.
        """
        subscription_query = gql(GET_NEW_BLOCK_SUBSCRIPTION)
        transport = WebsocketsTransport(url=self.subscription_url)
        try:
            async with Client(
                transport=transport,
                fetch_schema_from_transport=True,
            ) as session:
                async for result in session.subscribe(subscription_query):
                    yield result
        except Exception as e:
            logging.error("Subscription error: %s", e)
        finally:
            if hasattr(transport, "close"):
                await transport.close()
