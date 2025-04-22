# dnet/manager_factory.py

from dnet.Api.api_manager import ApiManager
from dnet.Coin.coin_manager import CoinManager
from dnet.Transaction.transaction_manager import TransactionManager
from dnet.Wallet.wallet_manager import WalletManager
from dnet.Explorer.explorer_manager import ExplorerManager
from dnet.User.user_manager import UserManager


class DNetManager:
    """
    Central manager that initializes all sub‑managers.
    Users need only supply their API key.
    """
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API_KEY is required to initialize DNetManager.")
        
        # HTTP base URL for standard GraphQL queries and mutations
        self.base_url = "http://203.0.113.2:8000/api"
        # WebSocket base URL for real‑time GraphQL subscriptions
        self.ws_base_url = "ws://203.0.113.2:8000/api/graphql/"
        
        # Use the HTTP URL for ApiManager that will be used for normal queries.
        self.api_manager = ApiManager(self.base_url, api_key)
        
        # Initialize sub‑managers with the appropriate ApiManager and URLs.
        self.wallet_manager = WalletManager(self.api_manager)
        self.user_manager = UserManager(self.api_manager)
        self.coin_manager = CoinManager(self.api_manager)
        self.transaction_manager = TransactionManager(self.api_manager)
        # ExplorerManager receives the same ApiManager (for HTTP queries)
        # and a dedicated WebSocket URL for subscriptions.
        self.explorer_manager = ExplorerManager(
            self.api_manager,
            subscription_url=self.ws_base_url
     
     
       )
    
    def get_wallet_manager(self):
        return self.wallet_manager
    
    def get_user_manager(self):
        return self.user_manager

    def get_coin_manager(self):
        return self.coin_manager

    def get_transaction_manager(self):
        return self.transaction_manager
    
    def get_explorer_manager(self):
        return self.explorer_manager

    # def get_user_manager(self):
    #     return self.user_manager

    # def get_wallet_manager(self):
    #     return self.wallet_manager

    # def get_coin_manager(self):
    #     return self.coin_manager

    # def get_transaction_manager(self):
    #     return self.transaction_manager
    
    # def get_explorer_manager(self):
    #     return self.explorer_manager
