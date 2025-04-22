from _typeshed import Incomplete
from bosa_core.authentication.config import AuthenticationDbSettings as AuthenticationDbSettings
from bosa_core.authentication.token.service.create_token_service import CreateTokenService as CreateTokenService
from bosa_core.authentication.token.storage.models import TokenComplete as TokenComplete
from bosa_core.authentication.token.storage.token_storage import TokenStorage as TokenStorage
from bosa_core.authentication.user.helper.helper import UserHelper as UserHelper
from bosa_core.authentication.user.service.get_user_service import GetUserService as GetUserService
from bosa_core.exception import UnauthorizedException as UnauthorizedException

class AuthenticateUserService:
    """Authenticate user service."""
    user_service: Incomplete
    user_helper: Incomplete
    create_token_service: Incomplete
    hash_service: Incomplete
    def __init__(self, token_storage: TokenStorage, user_service: GetUserService) -> None:
        """Initialize the service.

        Args:
            token_storage (TokenStorage): The token storage
            user_service (GetUserService): The user service
        """
    def authenticate_user(self, api_key: str, identifier: str, secret: str) -> TokenComplete:
        """Authenticate user.

        Args:
            api_key (str): The API key for client authentication
            identifier (str): The user identifier
            secret (str): The user secret

        Returns:
            TokenComplete: The token complete

        Raises:
            UnauthorizedException: If the user is not authenticated
        """
