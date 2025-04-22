
from dnet.Api.api_manager import ApiManager
from dnet.User.graphql_queries import (CREATE_USER_MUTATION,
    CREATE_COMPANY_MUTATION)

class UserManager:
    """
    A class to manage user-related operations via the network API using GraphQL.
    """

    def __init__(self, api_manager: ApiManager):
        """
        Initialize the WalletManager with an instance of ApiManager.
        :param api_manager: An instance of ApiManager for executing GraphQL operations.
        """
        self.api_manager = api_manager
        
    
    
    def create_user(self, email: str, password: str, organization: str = None):
        """
        Create a new user on the network.
        :param email: Email of the user.
        :param password: Password for the user.
        :param organization: Organization name (optional).
        :return: User creation response.
        """
        return self.api_manager._execute_graphql(
            CREATE_USER_MUTATION,
            {"email": email, "password": password, "organization": organization},
        )

    def create_company(self, name: str):
        """
        Create a new company on the network.
        :param name: Name of the company.
        :return: Company creation response.
        """
        return self.api_manager._execute_graphql(CREATE_COMPANY_MUTATION, {"name": name})