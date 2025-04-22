from _typeshed import Incomplete
from bosa_core.authentication.client.helper.helper import ClientHelper as ClientHelper
from bosa_core.authentication.client.service.verify_client_service import VerifyClientService as VerifyClientService
from bosa_core.authentication.client.storage.client_storage import ClientStorage as ClientStorage
from bosa_core.authentication.config import AuthenticationDbSettings as AuthenticationDbSettings
from bosa_core.authentication.token.storage.token_storage import TokenStorage as TokenStorage
from bosa_core.exception import InvalidClientException as InvalidClientException

class RevokeTokenService:
    """Revoke Token Service."""
    token_storage: Incomplete
    client_storage: Incomplete
    verify_client_service: Incomplete
    client_helper: Incomplete
    def __init__(self, token_storage: TokenStorage, client_storage: ClientStorage) -> None:
        """Initialize the service.

        Args:
            token_storage (TokenStorage): The token storage
            client_storage (ClientStorage): The client storage
        """
    def revoke_token(self, api_key: str, access_token: str) -> bool:
        """Revoke a token.

        Args:
            api_key: The API key for client authentication
            access_token: The JWT access token to revoke

        Returns:
            bool: True if token was found and revoked, False otherwise

        Raises:
            InvalidClientException: If client is not found or token is invalid
        """
