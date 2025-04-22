from _typeshed import Incomplete
from bosa_core.authentication.client.helper.helper import ClientHelper as ClientHelper
from bosa_core.authentication.client.service.client_aware_service import ClientAwareService as ClientAwareService
from bosa_core.authentication.client.service.verify_client_service import VerifyClientService as VerifyClientService
from bosa_core.authentication.client.storage.client_storage import ClientStorage as ClientStorage
from bosa_core.authentication.plugin.storage.models import ThirdPartyIntegrationAuthBasic as ThirdPartyIntegrationAuthBasic
from bosa_core.authentication.plugin.storage.storage import ThirdPartyIntegrationStorage as ThirdPartyIntegrationStorage
from bosa_core.authentication.user.storage.models import UserComplete as UserComplete, UserModel as UserModel
from bosa_core.authentication.user.storage.user_storage import UserStorage as UserStorage
from uuid import UUID

class GetUserService(ClientAwareService):
    """Get user service."""
    user_storage: Incomplete
    client_storage: Incomplete
    verify_client_service: Incomplete
    client_helper: Incomplete
    plugin_storage: Incomplete
    def __init__(self, user_storage: UserStorage, client_storage: ClientStorage, plugin_storage: ThirdPartyIntegrationStorage) -> None:
        """Initialize the service.

        Args:
            user_storage (UserStorage): The user storage
            client_storage (ClientStorage): The client storage
            plugin_storage (ThirdPartyIntegrationStorage): The plugin storage
        """
    def get_user(self, api_key: str, user_id: UUID) -> UserModel:
        """Get user.

        Args:
            api_key (str): The API key for client authentication
            user_id (UUID): The user ID

        Returns:
            UserModel: The user model

        Raises:
            InvalidClientException: If the client is not found
            UnauthorizedException: If the user is not found
        """
    def get_user_by_identifier(self, api_key: str, identifier: str) -> UserModel:
        """Get user by identifier.

        Args:
            api_key (str): The API key for client authentication
            identifier (str): The user identifier

        Returns:
            UserModel: The user model

        Raises:
            InvalidClientException: If the client is not found
            UnauthorizedException: If the user is not found
        """
    def get_user_complete(self, api_key: str, user_id: UUID) -> UserComplete:
        """Get user complete.

        Args:
            api_key (str): The API key for client authentication
            user_id (UUID): The user ID

        Returns:
            UserComplete: The user complete

        Raises:
            InvalidClientException: If the client is not found
            UnauthorizedException: If the user is not found
        """
