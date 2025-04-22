from _typeshed import Incomplete
from bosa_core.authentication.client.helper.helper import ClientHelper as ClientHelper
from bosa_core.authentication.client.service.verify_client_service import VerifyClientService as VerifyClientService
from bosa_core.authentication.client.storage.client_storage import ClientStorage as ClientStorage
from bosa_core.authentication.config import AuthenticationDbSettings as AuthenticationDbSettings
from bosa_core.authentication.token.storage.token_storage import TokenStorage as TokenStorage
from bosa_core.exception import InvalidClientException as InvalidClientException, UnauthorizedException as UnauthorizedException
from uuid import UUID

class VerifyTokenService:
    """Verify Token Service."""
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
    def verify_token_and_get_user_id(self, api_key: str, access_token: str) -> UUID:
        """Verify token and get user ID.

        Args:
            api_key (str): The API key for client authentication
            access_token (str): The JWT access token to verify

        Returns:
            UUID: The user ID

        Raises:
            InvalidClientException: If the client is not found
            JWTClaimsError: If the token claims are invalid
            ExpiredSignatureError: If the token has expired
        """
